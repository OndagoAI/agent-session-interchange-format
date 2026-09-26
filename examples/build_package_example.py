"""Reproduce a signed synthetic package. This public test key is never a trust anchor."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from reference.package import package_bytes, signature, inspect_package, verify_signature, MANIFEST
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
FOLDER=Path(__file__).resolve().parent
raw=package_bytes(FOLDER/'image-and-document.session.json')
key=Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
public=key.public_key().public_bytes_raw();sig=signature(raw,key.private_bytes_raw())
verify_signature(raw,sig,public)
(FOLDER/'package-example.asif.zip').write_bytes(raw)
(FOLDER/'package-signature.json').write_bytes(sig)
(FOLDER/'package-manifest.json').write_bytes(inspect_package(raw)[MANIFEST])
(FOLDER/'package-test-public.key').write_bytes(public)
print('Built reproducible synthetic package/signature; its test key is public, not trusted.')
