# ASIF package transport 0.1

Status: optional draft convention accompanying **ASIF 0.5**. [Specification](SPEC.md) · [Reference implementation](REFERENCE.md)

This envelope transports exact session JSON bytes and its file-backed embedded resources. It makes no continuation claim. ASIF documents can also be exchanged without an archive.

## Container

A package is an unencrypted ZIP containing regular files using `ZIP_STORED` (no compression). It MUST contain `session.json` and `asif-package.json`. Other members MUST be exactly the embedded resources referenced by relative `path` from the session. Inline text/base64 remain inside `session.json`. External content is not fetched.

Member names MUST be portable relative paths: no absolute paths, empty/dot/parent segments, backslashes, colons, control characters, Windows reserved device names, trailing dots/spaces, or `<>"|?*`. Names MUST NOT collide by case folding or have file/directory prefix collisions. Duplicate names, directory entries, symlinks, encrypted members, compressed members and unlisted files are rejected. `session.json` and `asif-package.json` are reserved resource paths.

The local writer sorts member names, uses the ZIP timestamp 1980-01-01 00:00:00 and regular-file mode 0600 for deterministic output. Readers validate inventory and resource closure before any extraction. The reference reader performs no extraction.

## Package Manifest Object

Inventories the exact bytes of every member except the manifest itself.

| Field | Type | Required | Description |
|---|---|---|---|
| `package_version` | string | Yes | Exactly `0.1`. |
| `session` | string | Yes | Exactly `session.json`. |
| `files` | array of [Package File Objects](#package-file-object) | Yes | Exactly one record for each non-manifest member. |

This example inventories the complete [attachment package](examples/package-example.asif.zip).

```json
{
  "files": [
    {
      "bytes": 90,
      "path": "assets/color-grid.png",
      "sha256": "9f557d344ce3af594e132efb0015748c336fb2daf0df7bd364f868fe5362affe"
    },
    {
      "bytes": 651,
      "path": "assets/meeting-notes.pdf",
      "sha256": "f73e34811d4480589c693aaf98f630c5478f786992f9410eeac4cb1b8144ed22"
    },
    {
      "bytes": 7652,
      "path": "session.json",
      "sha256": "eb8f249dad0a3adae72e2595a4e9705fa375ead9724d3eefc7eaae5bb02a22d9"
    }
  ],
  "package_version": "0.1",
  "session": "session.json"
}
```

## Package File Object

Binds a portable archive path to exact member bytes.

| Field | Type | Required | Description |
|---|---|---|---|
| `path` | string | Yes | Unique member name; cannot be `asif-package.json`. |
| `bytes` | integer | Yes | Exact uncompressed byte count. |
| `sha256` | string | Yes | Lowercase hexadecimal SHA-256 of those bytes. |

```json
{
  "path": "assets/hello.txt",
  "bytes": 3,
  "sha256": "98ea6e4f216f2fb4b69fff9b3a44842c38686ca685f3f55dc48c5d3fb1107be4"
}
```

The example bytes are UTF-8 `hi` followed by a newline.

## Detached Signature Object

A separate JSON file authenticates the manifest under a caller-supplied trusted Ed25519 public key. It is not a member of the package. The signed message is exactly:

```text
UTF8("ASIF-PACKAGE-MANIFEST-v1") || 0x00 || SHA256(exact manifest bytes)
```

The digest in that message is 32 binary bytes, not hexadecimal text. The manifest binds every transported file, including the exact source JSON. Reserializing the manifest changes the signed surface; no implicit JSON canonicalization is used during verification. A signature MUST NOT establish its own trust by providing an untrusted embedded public key.

| Field | Type | Required | Description |
|---|---|---|---|
| `signature_version` | string | Yes | Exactly `0.1`. |
| `algorithm` | string | Yes | Exactly `Ed25519`. |
| `manifest_sha256` | string | Yes | Lowercase hexadecimal digest of exact manifest bytes. |
| `key_id` | string | Yes | `sha256:` followed by the digest of the trusted raw 32-byte public key. |
| `signature` | string | Yes | Base64 encoding of the 64-byte signature. |

A complete generated example is in [package-signature.json](examples/package-signature.json), paired with the reproducible [package example recipe](examples/build_package_example.py). Its published key is a synthetic test key and MUST NOT be trusted for real data.

```json
{
  "algorithm": "Ed25519",
  "key_id": "sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c",
  "manifest_sha256": "f7b9987aec63a18d93ea4528d63f229434515ef15adb038b9d6b6bf20fe70d45",
  "signature": "8DO+94td8f0tgENs9L8oL8p+AoBUJqxC/1rSrDKe+77+Iig7cQ56EPXzsF+XLChpyZSUN6DnYhtDrjZsTuptDw==",
  "signature_version": "0.1"
}
```

## Meaning and limits

Successful signature verification authenticates these bytes under the supplied key. It does not prove the producer observed all activity, validate every session semantic rule, resolve external resources, or authorize continuation. Key distribution, revocation, encryption, remote storage and large-object chunking are outside this convention.

The [reference limits](REFERENCE.md#input-limits) constrain accepted package sizes and entry counts. These are declared implementation limits, not a universal maximum session size.
