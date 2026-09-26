/** Bounded ZIP32/STORED envelope; detached Ed25519 signatures use node:crypto. */
import * as fs from "node:fs";
import * as path from "node:path";
import { crc32 } from "node:zlib";
import {
  createPrivateKey,
  createPublicKey,
  sign as edSign,
  verify as edVerify,
} from "node:crypto";
import {
  type Obj,
  need,
  Invalid,
  Unsupported,
  decode,
  read,
  hash,
  relative,
  casefold,
  MAX_DOCUMENT,
  MAX_RESOURCE,
  MAX_TOTAL,
  utf8,
  base64,
  equal,
} from "./common.ts";
import { validateDocument, shape } from "./core.ts";
export const MANIFEST = "asif-package.json",
  MAX_MEMBERS = 1024,
  DOMAIN = Buffer.from("ASIF-PACKAGE-MANIFEST-v1\0");
function sorted(value: any): any {
  if (Array.isArray(value)) return value.map(sorted);
  if (value && typeof value === "object")
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .map((k) => [k, sorted(value[k])]),
    );
  return value;
}
const canonical = (v: any): Buffer =>
  Buffer.from(JSON.stringify(sorted(v)) + "\n");
export function zipStored(files: Map<string, Buffer>): Buffer {
  const locals: Buffer[] = [],
    centrals: Buffer[] = [];
  let offset = 0;
  need(files.size <= MAX_MEMBERS, "package member limit");
  for (const name of [...files.keys()].sort((a, b) =>
    Buffer.compare(Buffer.from(a), Buffer.from(b)),
  )) {
    const content = files.get(name)!,
      nameBytes = Buffer.from(name),
      flags = /[^\x00-\x7f]/.test(name) ? 0x800 : 0,
      crc = crc32(content),
      local = Buffer.alloc(30),
      central = Buffer.alloc(46);
    need(nameBytes.length <= 65535, "package name byte limit");
    local.writeUInt32LE(0x04034b50);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(flags, 6);
    local.writeUInt16LE(33, 12);
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(content.length, 18);
    local.writeUInt32LE(content.length, 22);
    local.writeUInt16LE(nameBytes.length, 26);
    central.writeUInt32LE(0x02014b50);
    central.writeUInt16LE(0x314, 4);
    central.writeUInt16LE(20, 6);
    central.writeUInt16LE(flags, 8);
    central.writeUInt16LE(33, 14);
    central.writeUInt32LE(crc, 16);
    central.writeUInt32LE(content.length, 20);
    central.writeUInt32LE(content.length, 24);
    central.writeUInt16LE(nameBytes.length, 28);
    central.writeUInt32LE((0o100600 << 16) >>> 0, 38);
    central.writeUInt32LE(offset, 42);
    locals.push(local, nameBytes, content);
    centrals.push(central, nameBytes);
    offset += local.length + nameBytes.length + content.length;
  }
  const directory = Buffer.concat(centrals),
    end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50);
  end.writeUInt16LE(files.size, 8);
  end.writeUInt16LE(files.size, 10);
  end.writeUInt32LE(directory.length, 12);
  end.writeUInt32LE(offset, 16);
  const result = Buffer.concat([...locals, directory, end]);
  need(result.length <= MAX_TOTAL + MAX_DOCUMENT, "package byte limit");
  return result;
}
export function packageBytes(source: string): Buffer {
  const raw = read(source),
    doc = decode(raw),
    v = validateDocument(doc, path.dirname(source)),
    files = new Map<string, Buffer>([["session.json", raw]]);
  for (const [id, r] of Object.entries<Obj>(v.resources.records))
    if (r.availability === "embedded" && Object.hasOwn(r, "path")) {
      need(
        !["session.json", MANIFEST].includes(casefold(r.path)),
        "reserved package path",
      );
      files.set(r.path, v.resources.bytes(id));
    }
  need(files.size + 1 <= MAX_MEMBERS, "package member limit");
  const inventory = [...files.keys()]
    .sort()
    .map((name) => ({
      path: name,
      bytes: files.get(name)!.length,
      sha256: hash(files.get(name)!),
    }));
  files.set(
    MANIFEST,
    canonical({
      package_version: "0.1",
      session: "session.json",
      files: inventory,
    }),
  );
  return zipStored(files);
}
export function inspectPackage(raw: Buffer): Map<string, Buffer> {
  need(raw.length <= MAX_TOTAL + MAX_DOCUMENT, "package byte limit");
  need(raw.length >= 22, "invalid ZIP container");
  let end = -1;
  for (let p = raw.length - 22; p >= Math.max(0, raw.length - 65557); p--)
    if (
      raw.readUInt32LE(p) === 0x06054b50 &&
      p + 22 + raw.readUInt16LE(p + 20) === raw.length
    ) {
      end = p;
      break;
    }
  need(end >= 0, "invalid ZIP container");
  const count = raw.readUInt16LE(end + 10),
    size = raw.readUInt32LE(end + 12),
    start = raw.readUInt32LE(end + 16);
  if (count === 65535 || size === 0xffffffff || start === 0xffffffff)
    throw new Unsupported("ZIP64 is not implemented in TypeScript");
  need(
    raw.readUInt16LE(end + 4) === 0 &&
      raw.readUInt16LE(end + 6) === 0 &&
      raw.readUInt16LE(end + 8) === count,
    "multidisk ZIP unsupported",
  );
  need(count <= MAX_MEMBERS, "package member limit");
  need(start + size === end, "invalid ZIP directory bounds");
  let p = start,
    total = 0;
  const files = new Map<string, Buffer>(),
    folded = new Set<string>(),
    ranges: [number, number][] = [];
  for (let i = 0; i < count; i++) {
    need(
      p + 46 <= end && raw.readUInt32LE(p) === 0x02014b50,
      "invalid ZIP directory",
    );
    const flags = raw.readUInt16LE(p + 8),
      method = raw.readUInt16LE(p + 10),
      crc = raw.readUInt32LE(p + 16),
      packed = raw.readUInt32LE(p + 20),
      length = raw.readUInt32LE(p + 24),
      nameLength = raw.readUInt16LE(p + 28),
      extra = raw.readUInt16LE(p + 30),
      comment = raw.readUInt16LE(p + 32),
      attrs = raw.readUInt32LE(p + 38),
      offset = raw.readUInt32LE(p + 42);
    need(method === 0 && !(flags & 1), "unsupported package encoding");
    if (flags & 8)
      throw new Unsupported(
        "ZIP data descriptors are not implemented in TypeScript",
      );
    need((flags & ~0x800) === 0, "unsupported ZIP flags");
    if ([packed, length, offset].includes(0xffffffff))
      throw new Unsupported("ZIP64 is not implemented in TypeScript");
    need(raw.readUInt16LE(p + 34) === 0, "multidisk ZIP unsupported");
    need(
      p + 46 + nameLength + extra + comment <= end,
      "invalid ZIP member bounds",
    );
    const nameRaw = raw.subarray(p + 46, p + 46 + nameLength);
    if (!(flags & 0x800) && nameRaw.some((c) => c > 127))
      throw new Unsupported(
        "legacy ZIP filename encoding is not implemented in TypeScript",
      );
    const name = utf8(nameRaw);
    relative(name);
    need(!folded.has(casefold(name)), "duplicate/colliding package member");
    folded.add(casefold(name));
    const mode = (attrs >>> 16) & 0o170000;
    need(
      !name.endsWith("/") && [0, 0o100000].includes(mode),
      "nonregular package member",
    );
    const limit = [MANIFEST, "session.json"].includes(name)
      ? MAX_DOCUMENT
      : MAX_RESOURCE;
    need(length <= limit, "package member byte limit");
    total += length;
    need(total <= MAX_TOTAL, "package total limit");
    need(packed === length, "package member size mismatch");
    need(
      offset + 30 <= start && raw.readUInt32LE(offset) === 0x04034b50,
      "invalid ZIP local header",
    );
    const localName = raw.readUInt16LE(offset + 26),
      localExtra = raw.readUInt16LE(offset + 28),
      dataStart = offset + 30 + localName + localExtra;
    need(dataStart + length <= start, "invalid ZIP payload bounds");
    need(
      raw.readUInt16LE(offset + 6) === flags &&
        raw.readUInt16LE(offset + 8) === method &&
        raw.readUInt32LE(offset + 14) === crc &&
        raw.readUInt32LE(offset + 18) === packed &&
        raw.readUInt32LE(offset + 22) === length,
      "ZIP local metadata mismatch",
    );
    need(
      raw.subarray(offset + 30, offset + 30 + localName).equals(nameRaw),
      "ZIP filename mismatch",
    );
    const content = raw.subarray(dataStart, dataStart + length);
    need(crc32(content) === crc, "ZIP CRC mismatch");
    ranges.push([offset, dataStart + length]);
    files.set(name, content);
    p += 46 + nameLength + extra + comment;
  }
  need(p === end, "invalid ZIP directory size");
  ranges.sort((a, b) => a[0] - b[0]);
  let cursor = 0;
  for (const [a, b] of ranges) {
    need(a === cursor, "overlapping or unlisted ZIP data");
    cursor = b;
  }
  need(cursor === start, "unlisted ZIP data");
  need(
    files.has(MANIFEST) && files.has("session.json"),
    "missing package metadata",
  );
  const manifest = decode(files.get(MANIFEST)!);
  need(
    manifest &&
      manifest.package_version === "0.1" &&
      manifest.session === "session.json",
    "unsupported package manifest",
  );
  need(Array.isArray(manifest.files), "invalid inventory");
  const seen = new Set<string>();
  for (const item of manifest.files) {
    need(
      item &&
        typeof item === "object" &&
        ["path", "bytes", "sha256"].every((k) => Object.hasOwn(item, k)),
      "invalid inventory record",
    );
    relative(item.path);
    need(item.path !== MANIFEST && !seen.has(item.path), "duplicate inventory");
    seen.add(item.path);
    need(files.has(item.path), "missing inventoried member");
    const content = files.get(item.path)!;
    need(
      Number.isInteger(item.bytes) && item.bytes === content.length,
      "inventory length mismatch",
    );
    need(item.sha256 === hash(content), "inventory digest mismatch");
  }
  need(
    equal(
      [...seen].sort(),
      [...files.keys()].filter((k) => k !== MANIFEST).sort(),
    ),
    "unlisted package member",
  );
  for (const name of files.keys())
    for (const other of files.keys())
      need(!other.startsWith(name + "/"), "package file/directory collision");
  const doc = decode(files.get("session.json")!);
  shape(doc);
  const expected = new Set(["session.json", MANIFEST]);
  for (const r of doc.resources)
    if (r.availability === "embedded" && Object.hasOwn(r, "path")) {
      relative(r.path);
      need(
        !["session.json", MANIFEST].includes(r.path),
        "reserved package resource path",
      );
      need(files.has(r.path), "missing packaged resource");
      const bytes = files.get(r.path)!;
      need(
        bytes.length === r.bytes && hash(bytes) === r.sha256,
        "packaged resource integrity",
      );
      expected.add(r.path);
    }
  need(
    equal([...expected].sort(), [...files.keys()].sort()),
    "package has unrelated files",
  );
  return files;
}
const privatePrefix = Buffer.from("302e020100300506032b657004220420", "hex"),
  publicPrefix = Buffer.from("302a300506032b6570032100", "hex");
export function signature(raw: Buffer, privateKey: Buffer): Buffer {
  const files = inspectPackage(raw),
    digest = hash(files.get(MANIFEST)!);
  need(privateKey.length === 32, "Ed25519 private key must be 32 bytes");
  const key = createPrivateKey({
      key: Buffer.concat([privatePrefix, privateKey]),
      format: "der",
      type: "pkcs8",
    }),
    publicKey = createPublicKey(key)
      .export({ format: "der", type: "spki" })
      .subarray(-32);
  return canonical({
    signature_version: "0.1",
    algorithm: "Ed25519",
    manifest_sha256: digest,
    key_id: "sha256:" + hash(publicKey),
    signature: edSign(
      null,
      Buffer.concat([DOMAIN, Buffer.from(digest, "hex")]),
      key,
    ).toString("base64"),
  });
}
export function verifySignature(
  raw: Buffer,
  rawSignature: Buffer,
  trustedKey: Buffer,
): Obj {
  const files = inspectPackage(raw),
    sig = decode(rawSignature),
    digest = hash(files.get(MANIFEST)!);
  need(
    sig?.signature_version === "0.1" && sig.algorithm === "Ed25519",
    "unsupported signature",
  );
  need(sig.manifest_sha256 === digest, "signed manifest mismatch");
  need(sig.key_id === "sha256:" + hash(trustedKey), "untrusted signing key");
  need(trustedKey.length === 32, "Ed25519 public key must be 32 bytes");
  let valid = false;
  try {
    const key = createPublicKey({
      key: Buffer.concat([publicPrefix, trustedKey]),
      format: "der",
      type: "spki",
    });
    valid = edVerify(
      null,
      Buffer.concat([DOMAIN, Buffer.from(digest, "hex")]),
      key,
      base64(sig.signature),
    );
  } catch {
    throw new Invalid("invalid package signature");
  }
  need(valid, "invalid package signature");
  return {
    status: "verified",
    key_id: sig.key_id,
    manifest_sha256: digest,
    scope:
      "package bytes under caller-supplied trusted key; no continuation claim",
  };
}
export function writeNew(file: string, content: Buffer): void {
  fs.writeFileSync(file, content, { flag: "wx", mode: 0o600 });
}
