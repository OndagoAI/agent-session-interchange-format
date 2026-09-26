# ASIF implementation evidence

Two locally authored reference implementations accompany **0.3**: [Python](asif.py) and [TypeScript](asif.ts). The TypeScript implementation ports the Python reference's documented subset and runs without Python. Both expose nine CLI commands; [scope and language differences](REFERENCE.md) remain explicit. Neither claims complete conformance or live agent continuation.

[TypeScript results](tests/typescript-results.json) include shared Python continuation expectations and local positive/negative tests. [Exchange results](tests/typescript-exchange-results.json) verify newly generated packages/signatures in both directions and compare CLI outputs and restored files. These implementations and tests share authorship; this does not satisfy the independent-implementation gate. Both reference implementations use the [MIT license](LICENSE).

**Independent implementations exchanging sessions: zero.**

Record actual participation only when an implementer supplies evidence:

- Project/repository, authors, affiliation, code revision and license terms.
- ASIF/profile versions, supported capabilities, limits and unsupported semantics.
- Fixture digests and reproducible commands/results.
- Independently produced sessions exchanged with another implementation.
- Results for structure, interpretation, interchange, context and continuation separately.
- Unresolved discrepancies and report location.
