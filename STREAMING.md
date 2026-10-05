# ASIF streaming and external bindings

Version: **0.4**. [Specification](SPEC.md) · [Stream Object](docs/objects.md#stream-object) · [External Binding Object](docs/objects.md#external-binding-object)

These optional features describe captured protocol evidence. They do not start streams, fetch older captures or execute tools.

## Stream assembly

`asif.streams/0.1` requires the root `streams` array. Each stream binds its `event_id` and `call_id` to a core tool event. `tool_result_text` additionally requires the exact `result_index`. Stream IDs are unique within the document. Segment indexes are nonnegative, unique and ordered. Segments select zero-based byte slices within declared embedded resources; byte spans MUST be in bounds.

Assembly concatenates segments by index starting at zero. A missing index leaves a partial stream; only the contiguous prefix is known to be assembled. At most one terminal segment is permitted, and it MUST be last. A stream is `complete` exactly when all indexes are contiguous from zero and its final segment is terminal. Empty streams are partial. Byte fragments may split UTF-8 sequences; decode only after assembly.

A complete `tool_arguments` stream MUST decode as UTF-8 JSON equal to its bound call's `arguments`, whose `arguments_status` MUST be `complete`. A partial argument stream MUST bind a call with `arguments_status: partial`. It cannot be used as an executable call. A complete `tool_result_text` stream MUST decode as UTF-8 and equal the bound result's single text part. The result's `terminal` flag closes the invocation; a stream's terminal segment closes only that stream.

The feature intentionally defines captured argument and text-result assembly. Other media or incremental protocols require a separately named feature and explicit loss reporting if translated.

An argument stream binds one immutable call **event version**, not whichever version of the invocation is currently selected. When partial arguments become complete in a later capture, retain the partial event and stream and create a new call amendment and stream under the [tool-call progression rules](SEMANTICS.md#tool-call-progression-across-captures). The new stream may reuse immutable fragment resources. It MUST agree with its own bound event; the earlier partial event and stream are not relabeled complete. Both streams share the invocation's `call_id` but have distinct stream and event IDs.

## External bindings

`asif.external-bindings/0.1` requires the root `external_bindings` array. A binding names one logical call or decision request outside the included event history, its exact source session/capture/event, and a typed descriptor. The source remains external history; a consumer MUST NOT synthesize an observed local event for it.

A call descriptor provides `tool_id`, `arguments` and `arguments_status`; its tool definition MUST be included locally. A request descriptor provides `decision_kind`, `prompt` and `options`. Its resource parts MUST reference declared resources. Option IDs are unique within the request. There can be only one binding per kind and identity, and a binding MUST NOT duplicate a local call/request identity.

A selected history may correlate a local result or resolution with such a binding. Missing bindings remain invalid for that interpretation. A model context still requires its own explicit, ordered typed inputs; an external binding is not permission to prepend an invented tool call to model input. Coverage and capture boundary declarations MUST disclose missing source history.

Amending the external invocation requires including its authentic predecessor event locally and removing the now-redundant binding for that invocation. The descriptor cannot stand in for the predecessor's event envelope or justify fabricating observed evidence. An unchanged external binding can still correlate a late result without a local call amendment.

## Examples

See [stream](docs/objects.md#stream-object), [segment](docs/objects.md#stream-segment-object), [external call](docs/objects.md#external-call-descriptor-object) and [external request](docs/objects.md#external-request-descriptor-object) examples. The [reference checks](tests/check_reference.py) include complete argument assembly, a missing segment, and a result whose call belongs to an earlier capture.
