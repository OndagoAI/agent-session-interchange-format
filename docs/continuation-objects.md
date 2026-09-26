# Continuation object reference

Version: **0.3**. [Specification](../SPEC.md) · [Core](objects.md) · [Continuation](continuation-objects.md) · [Reports](report-objects.md)

Every example below is JSON Schema checked. Object fragments use IDs resolved by an enclosing session or report; they are not standalone session documents. Full scenarios are in [examples](../examples/README.md). Required means unconditionally required; conditional rules follow each table. Normative [session semantics](../SEMANTICS.md) and [continuation rules](../CONTINUATION.md) also apply.

## Contents

- [Continuation Profile Object](continuation-objects.md#continuation-profile-object)
- [Agent Object](continuation-objects.md#agent-object)
- [Runtime Object](continuation-objects.md#runtime-object)
- [Runtime Adapter Object](continuation-objects.md#runtime-adapter-object)
- [Model Object](continuation-objects.md#model-object)
- [Workspace Entry Object](continuation-objects.md#workspace-entry-object)
- [Git State Object](continuation-objects.md#git-state-object)
- [Git Prerequisites Object](continuation-objects.md#git-prerequisites-object)
- [Git Index Entries Object](continuation-objects.md#git-index-entries-object)
- [Git Submodules Object](continuation-objects.md#git-submodules-object)
- [Workspace Object](continuation-objects.md#workspace-object)
- [Workspace Selection Object](continuation-objects.md#workspace-selection-object)
- [Tool Behavior Object](continuation-objects.md#tool-behavior-object)
- [Dependency Object](continuation-objects.md#dependency-object)
- [Dependency Platform Object](continuation-objects.md#dependency-platform-object)
- [Dependency Binding Object](continuation-objects.md#dependency-binding-object)
- [Scope Object](continuation-objects.md#scope-object)
- [Activation Object](continuation-objects.md#activation-object)
- [Configuration Binding Object](continuation-objects.md#configuration-binding-object)
- [Configuration Binding Instruction Rules Object](continuation-objects.md#configuration-binding-instruction-rules-object)
- [Service Binding Object](continuation-objects.md#service-binding-object)
- [Service Endpoint Object](continuation-objects.md#service-endpoint-object)
- [Service Account Object](continuation-objects.md#service-account-object)
- [Operation Object](continuation-objects.md#operation-object)
- [Operation External Identity Object](continuation-objects.md#operation-external-identity-object)
- [Operation Recovery Object](continuation-objects.md#operation-recovery-object)
- [Native Import Object](continuation-objects.md#native-import-object)
- [Native Adapter Object](continuation-objects.md#native-adapter-object)
- [Context Accounting Object](continuation-objects.md#context-accounting-object)
- [Next Action Object](continuation-objects.md#next-action-object)
- [Continuation Plan Object](continuation-objects.md#continuation-plan-object)
- [Plan Boundary Object](continuation-objects.md#plan-boundary-object)
- [Plan Cwd Object](continuation-objects.md#plan-cwd-object)
- [Plan Path References Object](continuation-objects.md#plan-path-references-object)
- [Plan Model Requirements Object](continuation-objects.md#plan-model-requirements-object)

<a id="continuation-profile-object"></a>

## Continuation Profile Object

Optional declarations needed to assess continuation from a session checkpoint. It contains no runtime authorization.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="continuation-profile-object-profile_version"></a>`profile_version` | `"0.1"` | Yes | Version of the portable-continuation profile. |
| <a id="continuation-profile-object-source_runtime"></a>`source_runtime` | [Runtime Object](continuation-objects.md#runtime-object) | Yes | Agent, adapter and platform recorded at the source. |
| <a id="continuation-profile-object-workspaces"></a>`workspaces` | array of [Workspace Object](continuation-objects.md#workspace-object) | Yes | Workspace state declarations, including referenced delta bases. Minimum items: `0`. |
| <a id="continuation-profile-object-dependencies"></a>`dependencies` | array of [Dependency Object](continuation-objects.md#dependency-object) | Yes | Declared dependencies; interpretation is determined by the enclosing object. Minimum items: `0`. |
| <a id="continuation-profile-object-configuration_bindings"></a>`configuration_bindings` | array of [Configuration Binding Object](continuation-objects.md#configuration-binding-object) | Yes | Portable interpretation bindings for configuration snapshots. Minimum items: `0`. |
| <a id="continuation-profile-object-service_bindings"></a>`service_bindings` | array of [Service Binding Object](continuation-objects.md#service-binding-object) | Yes | Service identity and access requirements. Minimum items: `0`. |
| <a id="continuation-profile-object-operations"></a>`operations` | array of [Operation Object](continuation-objects.md#operation-object) | Yes | Operations whose state or recovery matters to continuation. Minimum items: `0`. |
| <a id="continuation-profile-object-native_imports"></a>`native_imports` | array of [Native Import Object](continuation-objects.md#native-import-object) | Yes | Native-state import contracts, when required. Minimum items: `0`. |
| <a id="continuation-profile-object-plans"></a>`plans` | array of [Continuation Plan Object](continuation-objects.md#continuation-plan-object) | Yes | Selections of a checkpoint and its continuation prerequisites. Minimum items: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "profile_version": "0.1",
  "source_runtime": {
    "agent": {
      "id": "example-agent-a",
      "version": "1",
      "state_format": "example-native/1"
    },
    "adapter": {
      "id": "example-adapter",
      "version": "1"
    },
    "os": "macos",
    "architecture": "arm64"
  },
  "workspaces": [
    {
      "id": "workspace-head",
      "environment_id": "project-env",
      "root_id": "project",
      "at_event_id": "e4",
      "source_root": "/Users/example/project",
      "mode": "snapshot",
      "selection": {
        "include": [
          "inventory.csv",
          "totals.csv",
          "summary.md"
        ],
        "exclude": [
          ".cache/"
        ],
        "complete_for_selection": true
      },
      "entries": [
        {
          "path": "inventory.csv",
          "kind": "file",
          "mode": 420,
          "resource_id": "source-csv"
        },
        {
          "path": "totals.csv",
          "kind": "file",
          "mode": 420,
          "resource_id": "output-csv"
        },
        {
          "path": "summary.md",
          "kind": "file",
          "mode": 420,
          "resource_id": "report"
        }
      ],
      "deletions": [],
      "base_snapshot_id": null
    }
  ],
  "dependencies": [
    {
      "id": "agent-runtime",
      "kind": "agent_runtime",
      "identity": "example-agent-a",
      "accepted_versions": [
        "1"
      ],
      "platform": {
        "os": [
          "macos",
          "linux"
        ],
        "architectures": [
          "arm64",
          "x86_64"
        ]
      },
      "required_for": [
        "continue"
      ],
      "depends_on": [],
      "resource_ids": [],
      "binding": {
        "kind": "builtin",
        "reference": "example-agent-a"
      }
    },
    {
      "id": "summary-tool",
      "kind": "tool",
      "identity": "example.inventory.summarize",
      "accepted_versions": [
        "1"
      ],
      "platform": {
        "os": [
          "macos",
          "linux"
        ],
        "architectures": [
          "arm64",
          "x86_64"
        ]
      },
      "required_for": [
        "continue"
      ],
      "depends_on": [],
      "resource_ids": [],
      "binding": {
        "kind": "builtin",
        "reference": "example.inventory.summarize"
      },
      "tool_id": "summarize",
      "behavior": {
        "id": "example.inventory.summarize",
        "revision": "1",
        "effects": "local",
        "replay": "never"
      }
    },
    {
      "id": "summary-skill",
      "kind": "skill",
      "identity": "example.inventory-summary",
      "accepted_versions": [
        "1"
      ],
      "platform": {
        "os": [
          "macos",
          "linux"
        ],
        "architectures": [
          "arm64",
          "x86_64"
        ]
      },
      "required_for": [
        "continue"
      ],
      "depends_on": [
        "summary-tool"
      ],
      "resource_ids": [
        "skill-template"
      ],
      "binding": {
        "kind": "builtin",
        "reference": "example.inventory-summary"
      }
    }
  ],
  "configuration_bindings": [
    {
      "configuration_id": "effective",
      "effective_order": [
        "workspace-rule"
      ],
      "instruction_rules": [
        {
          "instruction_id": "workspace-rule",
          "authority": "system",
          "merge_behavior": "append",
          "group_id": "workspace-rules",
          "priority": 0,
          "scope": {
            "kind": "root",
            "root_id": "project"
          },
          "activation": {
            "kind": "always"
          }
        }
      ],
      "policy_ids": [
        "workspace-only"
      ]
    }
  ],
  "service_bindings": [],
  "operations": [],
  "native_imports": [
    {
      "id": "native",
      "adapter": {
        "id": "example-adapter",
        "version": "1"
      },
      "source_state_format": "example-native/1",
      "accepted_target_agent_versions": [
        "1"
      ],
      "resource_ids": [
        "native-state"
      ],
      "mode": "continue",
      "identity_policy": "preserve_if_safe",
      "ordering_contract": "example.ordinal-order/1",
      "index_contract": "example.native-index/1",
      "conflict_policy": "reject"
    }
  ],
  "plans": [
    {
      "id": "continue-main",
      "checkpoint_id": "head",
      "context_id": "continue-context",
      "configuration_id": "effective",
      "workspace_ids": [
        "workspace-head"
      ],
      "dependency_ids": [
        "agent-runtime",
        "summary-tool",
        "summary-skill"
      ],
      "service_binding_ids": [],
      "operation_ids": [],
      "native_import_id": "native",
      "boundary": {
        "method": "quiesced",
        "consistency": "consistent",
        "evidence_resource_ids": [],
        "explanation": "Invented quiescent source checkpoint; illustrative evidence only."
      },
      "context_accounting": [
        {
          "event_id": "e1",
          "disposition": "included",
          "input_ids": [
            "input-e1"
          ],
          "explanation": "Retained as a typed input in the reconstructed continuation context."
        },
        {
          "event_id": "e2",
          "disposition": "included",
          "input_ids": [
            "input-e2"
          ],
          "explanation": "Retained as a typed input in the reconstructed continuation context."
        },
        {
          "event_id": "e3",
          "disposition": "included",
          "input_ids": [
            "input-e3"
          ],
          "explanation": "Retained as a typed input in the reconstructed continuation context."
        },
        {
          "event_id": "e4",
          "disposition": "included",
          "input_ids": [
            "input-e4"
          ],
          "explanation": "Retained as a typed input in the reconstructed continuation context."
        }
      ],
      "cwd": {
        "root_id": "project",
        "relative_path": ""
      },
      "path_references": [
        {
          "entity_type": "environment",
          "entity_id": "project-env",
          "json_pointer": "/definition/value/cwd",
          "root_id": "project",
          "relative_path": ""
        }
      ],
      "model_requirements": {
        "source_model": {
          "provider": "example",
          "id": "model-a",
          "revision": "1"
        },
        "capabilities": [
          "text",
          "tool_calls"
        ],
        "media_types": [
          "text/csv",
          "text/markdown"
        ],
        "overflow_policy": "block"
      },
      "next_action": {
        "kind": "await_user"
      }
    }
  ]
}
```

<a id="agent-object"></a>

## Agent Object

Names an agent implementation, version and native state format.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="agent-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="agent-object-version"></a>`version` | string / null | Yes | Implementation or format version. |
| <a id="agent-object-state_format"></a>`state_format` | string / null | Yes | Native state-format identifier. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "example-agent-b",
  "version": "2",
  "state_format": "example-b/2"
}
```

<a id="runtime-object"></a>

## Runtime Object

Identifies the agent, adapter and operating platform involved in a continuation assessment.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="runtime-object-agent"></a>`agent` | [Agent Object](continuation-objects.md#agent-object) | Yes | Agent implementation, version and state format. |
| <a id="runtime-object-adapter"></a>`adapter` | [Runtime Adapter Object](continuation-objects.md#runtime-adapter-object) | Yes | Adapter implementation and version interpreting the source or destination. |
| <a id="runtime-object-os"></a>`os` | string | Yes | Operating-system identifier or accepted identifiers. Minimum length: `1`. |
| <a id="runtime-object-architecture"></a>`architecture` | string | Yes | Runtime CPU architecture identifier. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "agent": {
    "id": "example-agent-b",
    "version": "2",
    "state_format": "example-b/2"
  },
  "adapter": {
    "id": "example-a-to-b",
    "version": "1"
  },
  "os": "linux",
  "architecture": "x86_64"
}
```

<a id="runtime-adapter-object"></a>

## Runtime Adapter Object

Names the adapter implementation and version used to interpret native state.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="runtime-adapter-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="runtime-adapter-object-version"></a>`version` | string / null | Yes | Implementation or format version. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "example-a-to-b",
  "version": "1"
}
```

<a id="model-object"></a>

## Model Object

Identifies a model provider, model ID and optional known revision without assuming equivalence to another model.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="model-object-provider"></a>`provider` | string | Yes | Provider identity for the named object or account. Minimum length: `1`. |
| <a id="model-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="model-object-revision"></a>`revision` | string / null | Yes | Versioned definition or task revision within its identity. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "provider": "example",
  "id": "model-a",
  "revision": "1"
}
```

<a id="workspace-entry-object"></a>

## Workspace Entry Object

One selected filesystem entry. File bytes are resources; link targets are declarations requiring a destination link policy.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="workspace-entry-object-path"></a>`path` | string | Yes | Portable relative path within the declared resource or workspace root. Minimum length: `1`. |
| <a id="workspace-entry-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"file"`, `"directory"`, `"symlink"`. |
| <a id="workspace-entry-object-mode"></a>`mode` | integer | No | POSIX permission bits expressed as a decimal integer, from 0 through 511 (octal 0777). Minimum: `0`. Maximum: `511`. |
| <a id="workspace-entry-object-resource_id"></a>`resource_id` | string | No | ID of the referenced Resource Object. Minimum length: `1`. |
| <a id="workspace-entry-object-target"></a>`target` | string | No | Declared target value, model or symbolic-link target according to context. Minimum length: `1`. |

### Rules

See [workspace rules](../CONTINUATION.md#5-workspace-snapshots-roots-and-paths). A file requires mode and resource_id; a directory requires mode; a symlink requires target. The local reference restorer explicitly refuses symlinks.

- When `kind` is `"file"`, require `mode`, `resource_id`.
- When `kind` is `"directory"`, require `mode`.
- When `kind` is `"symlink"`, require `target`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "path": "summary.md",
  "kind": "file",
  "mode": 420,
  "resource_id": "report"
}
```

<a id="git-state-object"></a>

## Git State Object

Describes Git identity, index stages, object prerequisites, submodules and LFS dependencies separately from working-tree bytes.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="git-state-object-object_format"></a>`object_format` | string | Yes | Git object hash algorithm. Minimum length: `1`. |
| <a id="git-state-object-head"></a>`head` | string / null | Yes | Captured Git HEAD object ID, or null if unavailable or unborn. |
| <a id="git-state-object-branch"></a>`branch` | string / null | Yes | Captured Git branch name, or null for no named branch. |
| <a id="git-state-object-bundle_resource_ids"></a>`bundle_resource_ids` | array of string | Yes | Resources carrying Git bundles required by the declaration. Minimum items: `0`. Items MUST be unique. |
| <a id="git-state-object-prerequisites"></a>`prerequisites` | array of [Git Prerequisites Object](continuation-objects.md#git-prerequisites-object) | Yes | Git objects that must be resolved before restoration. Minimum items: `0`. |
| <a id="git-state-object-index_entries"></a>`index_entries` | array of [Git Index Entries Object](continuation-objects.md#git-index-entries-object) | Yes | Per-path Git index stages, separate from the working tree. Minimum items: `0`. |
| <a id="git-state-object-submodules"></a>`submodules` | array of [Git Submodules Object](continuation-objects.md#git-submodules-object) | Yes | Submodule paths, pinned objects and dependency bindings. Minimum items: `0`. |
| <a id="git-state-object-lfs_dependency_ids"></a>`lfs_dependency_ids` | array of string | Yes | Dependencies needed to resolve Git LFS content. Minimum items: `0`. Items MUST be unique. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "object_format": "example",
  "head": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "branch": "main",
  "bundle_resource_ids": [],
  "prerequisites": [],
  "index_entries": [],
  "submodules": [],
  "lfs_dependency_ids": []
}
```

<a id="git-prerequisites-object"></a>

## Git Prerequisites Object

Declares a Git object required to interpret or restore the captured state.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="git-prerequisites-object-object_id"></a>`object_id` | string | Yes | Git object ID in the declared object format, when known. Minimum length: `1`. |
| <a id="git-prerequisites-object-availability"></a>`availability` | enum | Yes | Whether and how the referenced content is available. One of `"embedded"`, `"external"`, `"unavailable"`, `"unknown"`. |
| <a id="git-prerequisites-object-resource_id"></a>`resource_id` | string | No | ID of the referenced Resource Object. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "object_id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
  "availability": "external"
}
```

<a id="git-index-entries-object"></a>

## Git Index Entries Object

Records one index path and stage, preserving conflicts rather than collapsing them into working-tree content.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="git-index-entries-object-path"></a>`path` | string | Yes | Portable relative path within the declared resource or workspace root. Minimum length: `1`. |
| <a id="git-index-entries-object-stage"></a>`stage` | integer | Yes | Transformation stage; in a Git index entry, the conflict stage number. Minimum: `0`. Maximum: `3`. |
| <a id="git-index-entries-object-mode"></a>`mode` | string | Yes | Representation or interpretation mode selected by the enclosing object. Minimum length: `1`. |
| <a id="git-index-entries-object-resource_id"></a>`resource_id` | string / null | Yes | ID of the referenced Resource Object. |
| <a id="git-index-entries-object-object_id"></a>`object_id` | string / null | Yes | Git object ID in the declared object format, when known. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "path": "notes.md",
  "stage": 0,
  "mode": "100644",
  "resource_id": "notes",
  "object_id": null
}
```

<a id="git-submodules-object"></a>

## Git Submodules Object

Pins a submodule path and commit and names the dependency needed to resolve it.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="git-submodules-object-path"></a>`path` | string | Yes | Portable relative path within the declared resource or workspace root. Minimum length: `1`. |
| <a id="git-submodules-object-object_id"></a>`object_id` | string | Yes | Git object ID in the declared object format, when known. Minimum length: `1`. |
| <a id="git-submodules-object-dependency_id"></a>`dependency_id` | string | Yes | ID of the referenced dependency declaration. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "path": "vendor/library",
  "object_id": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
  "dependency_id": "dependency-library"
}
```

<a id="workspace-object"></a>

## Workspace Object

A selected filesystem snapshot, delta or reference declaration bound to a session boundary and logical root.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="workspace-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="workspace-object-environment_id"></a>`environment_id` | string | Yes | Referenced Environment Object ID. Minimum length: `1`. |
| <a id="workspace-object-root_id"></a>`root_id` | string | Yes | Logical workspace root identity, independent of source and destination absolute paths. Minimum length: `1`. |
| <a id="workspace-object-at_event_id"></a>`at_event_id` | string / null | Yes | Event at the recorded boundary, or null for an empty boundary. |
| <a id="workspace-object-source_root"></a>`source_root` | string | Yes | Recorded source path, retained as metadata. Minimum length: `1`. |
| <a id="workspace-object-mode"></a>`mode` | enum | Yes | Representation or interpretation mode selected by the enclosing object. One of `"snapshot"`, `"delta"`, `"refs"`. |
| <a id="workspace-object-selection"></a>`selection` | [Workspace Selection Object](continuation-objects.md#workspace-selection-object) | Yes | Included and excluded workspace paths and completeness within that selection. |
| <a id="workspace-object-entries"></a>`entries` | array of [Workspace Entry Object](continuation-objects.md#workspace-entry-object) | Yes | Explicit filesystem entries captured by this workspace declaration. Minimum items: `0`. |
| <a id="workspace-object-deletions"></a>`deletions` | array of string | Yes | Paths explicitly removed by a delta; absence alone is not deletion. Minimum items: `0`. |
| <a id="workspace-object-base_snapshot_id"></a>`base_snapshot_id` | string / null | Yes | ID of the included base state, or null when no base is required. |
| <a id="workspace-object-git"></a>`git` | [Git State Object](continuation-objects.md#git-state-object) | No | Optional Git administrative and object prerequisites, separate from selected files. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

- When `mode` is `"refs"`, require `git`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "workspace-head",
  "environment_id": "project-env",
  "root_id": "project",
  "at_event_id": "e4",
  "source_root": "/Users/example/project",
  "mode": "snapshot",
  "selection": {
    "include": [
      "inventory.csv",
      "totals.csv",
      "summary.md"
    ],
    "exclude": [
      ".cache/"
    ],
    "complete_for_selection": true
  },
  "entries": [
    {
      "path": "inventory.csv",
      "kind": "file",
      "mode": 420,
      "resource_id": "source-csv"
    },
    {
      "path": "totals.csv",
      "kind": "file",
      "mode": 420,
      "resource_id": "output-csv"
    },
    {
      "path": "summary.md",
      "kind": "file",
      "mode": 420,
      "resource_id": "report"
    }
  ],
  "deletions": [],
  "base_snapshot_id": null
}
```

<a id="workspace-selection-object"></a>

## Workspace Selection Object

Defines the selected portion of a workspace and whether it is complete within that selection.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="workspace-selection-object-include"></a>`include` | array of string | Yes | Declared include patterns for the selected workspace tree. Minimum items: `0`. |
| <a id="workspace-selection-object-exclude"></a>`exclude` | array of string | Yes | Declared excluded paths or patterns, protected from implicit deletion. Minimum items: `0`. |
| <a id="workspace-selection-object-complete_for_selection"></a>`complete_for_selection` | boolean | Yes | Whether every entry within the declared selection is accounted for. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "include": [
    "inventory.csv",
    "totals.csv",
    "summary.md"
  ],
  "exclude": [
    ".cache/"
  ],
  "complete_for_selection": true
}
```

<a id="tool-behavior-object"></a>

## Tool Behavior Object

Describes a versioned tool behavior contract, including effects and replay semantics.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="tool-behavior-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="tool-behavior-object-revision"></a>`revision` | string | Yes | Versioned definition or task revision within its identity. Minimum length: `1`. |
| <a id="tool-behavior-object-effects"></a>`effects` | enum | Yes | Known side-effect classes of the tool or operation. One of `"none"`, `"local"`, `"remote"`, `"unknown"`. |
| <a id="tool-behavior-object-replay"></a>`replay` | enum | Yes | Declared replay characteristics; unknown never implies safe repetition. One of `"never"`, `"idempotent"`, `"reconcile"`, `"unknown"`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "example.inventory.summarize",
  "revision": "1",
  "effects": "local",
  "replay": "never"
}
```

<a id="dependency-object"></a>

## Dependency Object

A runtime, tool, capability or other dependency with explicit version, platform and transitive requirements.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="dependency-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="dependency-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"agent_runtime"`, `"model"`, `"executable"`, `"package"`, `"skill"`, `"plugin"`, `"hook"`, `"tool"`, `"policy"`, `"service"`, `"resource"`. |
| <a id="dependency-object-identity"></a>`identity` | string | Yes | Namespaced dependency identity to resolve. Minimum length: `1`. |
| <a id="dependency-object-accepted_versions"></a>`accepted_versions` | array of string | Yes | Explicit accepted dependency versions; not a guessed compatibility range. Minimum items: `0`. Items MUST be unique. |
| <a id="dependency-object-platform"></a>`platform` | [Dependency Platform Object](continuation-objects.md#dependency-platform-object) | Yes | Operating-system and architecture constraints. |
| <a id="dependency-object-required_for"></a>`required_for` | array of enum | Yes | Capabilities that depend on this prerequisite. Minimum items: `0`. Items MUST be unique. |
| <a id="dependency-object-depends_on"></a>`depends_on` | array of string | Yes | Dependency IDs required transitively by this declaration. Minimum items: `0`. Items MUST be unique. |
| <a id="dependency-object-resource_ids"></a>`resource_ids` | array of string | Yes | IDs of supporting resources; their availability is declared separately. Minimum items: `0`. Items MUST be unique. |
| <a id="dependency-object-binding"></a>`binding` | [Dependency Binding Object](continuation-objects.md#dependency-binding-object) | Yes | Resolution mechanism and reference for the dependency. |
| <a id="dependency-object-tool_id"></a>`tool_id` | string | No | ID of the referenced tool definition. Minimum length: `1`. |
| <a id="dependency-object-behavior"></a>`behavior` | [Tool Behavior Object](continuation-objects.md#tool-behavior-object) | No | Versioned behavior and side-effect contract for a tool. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

- When `kind` is `"tool"`, require `tool_id`, `behavior`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "agent-runtime",
  "kind": "agent_runtime",
  "identity": "example-agent-a",
  "accepted_versions": [
    "1"
  ],
  "platform": {
    "os": [
      "macos",
      "linux"
    ],
    "architectures": [
      "arm64",
      "x86_64"
    ]
  },
  "required_for": [
    "continue"
  ],
  "depends_on": [],
  "resource_ids": [],
  "binding": {
    "kind": "builtin",
    "reference": "example-agent-a"
  }
}
```

<a id="dependency-platform-object"></a>

## Dependency Platform Object

Declares the operating systems and architectures on which the dependency is accepted.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="dependency-platform-object-os"></a>`os` | array of string | Yes | Operating-system identifier or accepted identifiers. Minimum items: `0`. Items MUST be unique. |
| <a id="dependency-platform-object-architectures"></a>`architectures` | array of string | Yes | Accepted CPU architecture identifiers. Minimum items: `0`. Items MUST be unique. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "os": [
    "macos",
    "linux"
  ],
  "architectures": [
    "arm64",
    "x86_64"
  ]
}
```

<a id="dependency-binding-object"></a>

## Dependency Binding Object

Describes how a dependency is expected to be resolved without installing or fetching it automatically.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="dependency-binding-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"builtin"`, `"package"`, `"command"`, `"service"`, `"opaque"`. |
| <a id="dependency-binding-object-reference"></a>`reference` | string | Yes | Opaque evidence or resolution locator; no implicit fetch is permitted. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "builtin",
  "reference": "example-agent-a"
}
```

<a id="scope-object"></a>

## Scope Object

A portable instruction scope: global, a logical root or a path prefix within that root.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="scope-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"global"`, `"root"`, `"path_prefix"`. |
| <a id="scope-object-root_id"></a>`root_id` | string | No | Logical workspace root identity, independent of source and destination absolute paths. Minimum length: `1`. |
| <a id="scope-object-relative_path"></a>`relative_path` | string | No | Portable path relative to the named logical root. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

- When `kind` is `"root"`, require `root_id`.
- When `kind` is `"path_prefix"`, require `root_id`, `relative_path`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "root",
  "root_id": "project"
}
```

<a id="activation-object"></a>

## Activation Object

An unconditional activation or a predicate in an explicitly named dialect.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="activation-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"always"`, `"predicate"`. |
| <a id="activation-object-dialect"></a>`dialect` | string | No | Identifier of the language used to interpret the associated value. Minimum length: `1`. |
| <a id="activation-object-expression"></a>`expression` | JSON value | No | Predicate value interpreted only by the explicitly named activation dialect. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

- When `kind` is `"predicate"`, require `dialect`, `expression`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "always"
}
```

<a id="configuration-binding-object"></a>

## Configuration Binding Object

Connects a configuration to explicit instruction order, interpretation rules and policy identities.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="configuration-binding-object-configuration_id"></a>`configuration_id` | string | Yes | ID of the configuration snapshot used at this boundary. Minimum length: `1`. |
| <a id="configuration-binding-object-effective_order"></a>`effective_order` | array of string | Yes | Exact order of instruction IDs after precedence resolution. Minimum items: `0`. Items MUST be unique. |
| <a id="configuration-binding-object-instruction_rules"></a>`instruction_rules` | array of [Configuration Binding Instruction Rules Object](continuation-objects.md#configuration-binding-instruction-rules-object) | Yes | One interpretation rule for each instruction in the bound configuration. Minimum items: `0`. |
| <a id="configuration-binding-object-policy_ids"></a>`policy_ids` | array of string | Yes | Policy IDs scoped to the bound configuration. Minimum items: `0`. Items MUST be unique. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "configuration_id": "effective",
  "effective_order": [],
  "instruction_rules": [],
  "policy_ids": []
}
```

<a id="configuration-binding-instruction-rules-object"></a>

## Configuration Binding Instruction Rules Object

Declares one instruction's authority, merge behavior, priority, scope and activation.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="configuration-binding-instruction-rules-object-instruction_id"></a>`instruction_id` | string | Yes | Instruction ID within the bound configuration. Minimum length: `1`. |
| <a id="configuration-binding-instruction-rules-object-authority"></a>`authority` | enum | Yes | Declared authority of the instruction; an unknown value blocks equivalence claims. One of `"system"`, `"developer"`, `"user"`, `"untrusted"`, `"unknown"`. |
| <a id="configuration-binding-instruction-rules-object-merge_behavior"></a>`merge_behavior` | enum | Yes | How this instruction combines with others in the same declared scope and group. One of `"append"`, `"replace_same_scope"`, `"reject_conflict"`, `"unknown"`. |
| <a id="configuration-binding-instruction-rules-object-group_id"></a>`group_id` | string | Yes | Identity of the instruction merge group. Minimum length: `1`. |
| <a id="configuration-binding-instruction-rules-object-priority"></a>`priority` | integer | Yes | Precedence value; effective order must agree with ascending priority. |
| <a id="configuration-binding-instruction-rules-object-scope"></a>`scope` | [Scope Object](continuation-objects.md#scope-object) | Yes | Domain or activation scope to which this declaration applies. |
| <a id="configuration-binding-instruction-rules-object-activation"></a>`activation` | [Activation Object](continuation-objects.md#activation-object) | Yes | Conditions under which an instruction or rule applies. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "instruction_id": "workspace-rule",
  "authority": "system",
  "merge_behavior": "append",
  "group_id": "workspace-rules",
  "priority": 0,
  "scope": {
    "kind": "root",
    "root_id": "project"
  },
  "activation": {
    "kind": "always"
  }
}
```

<a id="service-binding-object"></a>

## Service Binding Object

Describes the service identity and access prerequisites that a destination must resolve separately.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="service-binding-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="service-binding-object-service"></a>`service` | string | Yes | Namespaced service identity. Minimum length: `1`. |
| <a id="service-binding-object-endpoint"></a>`endpoint` | [Service Endpoint Object](continuation-objects.md#service-endpoint-object) | Yes | Recorded or resolved endpoint declaration. |
| <a id="service-binding-object-account"></a>`account` | [Service Account Object](continuation-objects.md#service-account-object) | Yes | Expected or resolved service-account identity. |
| <a id="service-binding-object-auth_method"></a>`auth_method` | enum | Yes | Required authentication mechanism, without credentials. One of `"none"`, `"api_key"`, `"oauth"`, `"login"`, `"other"`. |
| <a id="service-binding-object-audience"></a>`audience` | string | Yes | Intended service audience for access credentials. Minimum length: `1`. |
| <a id="service-binding-object-scopes"></a>`scopes` | array of string | Yes | Required or resolved service access scopes. Minimum items: `0`. Items MUST be unique. |
| <a id="service-binding-object-secret_handles"></a>`secret_handles` | array of string | Yes | Logical credential handles to resolve separately at the destination. Minimum items: `0`. Items MUST be unique. |
| <a id="service-binding-object-dependency_ids"></a>`dependency_ids` | array of string | Yes | IDs of selected dependencies; selected closure must be complete. Minimum items: `0`. Items MUST be unique. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "publisher-service",
  "service": "example.publisher",
  "endpoint": {
    "kind": "https",
    "locator": "https://publisher.example.invalid"
  },
  "account": {
    "provider": "example",
    "subject": "account-A"
  },
  "auth_method": "oauth",
  "audience": "example.publisher",
  "scopes": [
    "reports:write"
  ],
  "secret_handles": [
    "publisher-login"
  ],
  "dependency_ids": [
    "publisher"
  ]
}
```

<a id="service-endpoint-object"></a>

## Service Endpoint Object

A recorded service locator or destination-resolved endpoint declaration.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="service-endpoint-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"https"`, `"stdio"`, `"local_socket"`, `"other"`. |
| <a id="service-endpoint-object-locator"></a>`locator` | string | Yes | Location interpreted according to its declared syntax or availability. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "https",
  "locator": "https://publisher.example.invalid"
}
```

<a id="service-account-object"></a>

## Service Account Object

Identifies the expected account without including credentials.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="service-account-object-provider"></a>`provider` | string | Yes | Provider identity for the named object or account. Minimum length: `1`. |
| <a id="service-account-object-subject"></a>`subject` | string | Yes | Account identity or assessed subject, as defined by the containing object. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "provider": "example",
  "subject": "account-A"
}
```

<a id="operation-object"></a>

## Operation Object

Records an external or local operation whose outcome or recovery affects continuation.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="operation-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="operation-object-call_id"></a>`call_id` | string | No | Session-scoped identity of one logical invocation. Minimum length: `1`. |
| <a id="operation-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"tool"`, `"process"`, `"service_job"`, `"agent"`. |
| <a id="operation-object-external_identity"></a>`external_identity` | [Operation External Identity Object](continuation-objects.md#operation-external-identity-object) / null | Yes | Identifier used to reconcile this operation in its external system. |
| <a id="operation-object-state"></a>`state` | enum | Yes | Recorded pending or observed state; it is not a live process assertion. One of `"pending"`, `"running"`, `"succeeded"`, `"failed"`, `"cancelled"`, `"outcome_unknown"`. |
| <a id="operation-object-effects"></a>`effects` | enum | Yes | Known side-effect classes of the tool or operation. One of `"none"`, `"local"`, `"remote"`, `"unknown"`. |
| <a id="operation-object-replay"></a>`replay` | enum | Yes | Declared replay characteristics; unknown never implies safe repetition. One of `"never"`, `"idempotent"`, `"reconcile"`, `"unknown"`. |
| <a id="operation-object-evidence_resource_ids"></a>`evidence_resource_ids` | array of string | Yes | Resources supporting the claim or recovery declaration. Minimum items: `0`. Items MUST be unique. |
| <a id="operation-object-recovery"></a>`recovery` | [Operation Recovery Object](continuation-objects.md#operation-recovery-object) | Yes | Declared strategy for resolving or recovering the operation. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

- When `kind` is `"tool"`, require `call_id`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "publish-operation",
  "call_id": "call-1",
  "kind": "tool",
  "external_identity": {
    "namespace": "example.publisher/account-A",
    "value": "operation-42"
  },
  "state": "outcome_unknown",
  "effects": "remote",
  "replay": "reconcile",
  "evidence_resource_ids": [],
  "recovery": {
    "strategy": "reconcile",
    "handler_dependency_id": "publisher",
    "idempotency_ref": null,
    "evidence_resource_ids": []
  }
}
```

<a id="operation-external-identity-object"></a>

## Operation External Identity Object

Names an operation in an external system without treating its identifier as proof of status.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="operation-external-identity-object-namespace"></a>`namespace` | string | Yes | Namespace in which the opaque value is meaningful. Minimum length: `1`. |
| <a id="operation-external-identity-object-value"></a>`value` | string | Yes | Value interpreted according to the enclosing schema, dialect or counter. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "namespace": "example.publisher/account-A",
  "value": "operation-42"
}
```

<a id="operation-recovery-object"></a>

## Operation Recovery Object

Declares a recovery strategy and its required handler, idempotency binding and evidence.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="operation-recovery-object-strategy"></a>`strategy` | enum | Yes | Recovery action supported by the declared evidence and handler. One of `"reconcile"`, `"reconnect"`, `"restart"`, `"refuse"`. |
| <a id="operation-recovery-object-handler_dependency_id"></a>`handler_dependency_id` | string / null | Yes | Dependency implementing recovery, or null when no handler is selected. |
| <a id="operation-recovery-object-idempotency_ref"></a>`idempotency_ref` | string / null | Yes | Recorded idempotency binding, when available; not an authorization to replay. |
| <a id="operation-recovery-object-evidence_resource_ids"></a>`evidence_resource_ids` | array of string | Yes | Resources supporting the claim or recovery declaration. Minimum items: `0`. Items MUST be unique. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "strategy": "reconcile",
  "handler_dependency_id": "publisher",
  "idempotency_ref": null,
  "evidence_resource_ids": []
}
```

<a id="native-import-object"></a>

## Native Import Object

Describes a native-state import contract, including ordering, indexes, identity and conflicts.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="native-import-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="native-import-object-adapter"></a>`adapter` | [Native Adapter Object](continuation-objects.md#native-adapter-object) | Yes | Adapter implementation and version interpreting the source or destination. |
| <a id="native-import-object-source_state_format"></a>`source_state_format` | string | Yes | Native source format expected by the import adapter. Minimum length: `1`. |
| <a id="native-import-object-accepted_target_agent_versions"></a>`accepted_target_agent_versions` | array of string | Yes | Explicit target versions supported by this import contract. Minimum items: `0`. Items MUST be unique. |
| <a id="native-import-object-resource_ids"></a>`resource_ids` | array of string | Yes | IDs of supporting resources; their availability is declared separately. Minimum items: `0`. Items MUST be unique. |
| <a id="native-import-object-mode"></a>`mode` | enum | Yes | Representation or interpretation mode selected by the enclosing object. One of `"copy"`, `"continue"`, `"translate"`. |
| <a id="native-import-object-identity_policy"></a>`identity_policy` | enum | Yes | How native identities are preserved or mapped during import. One of `"new"`, `"preserve_if_safe"`, `"map"`. |
| <a id="native-import-object-ordering_contract"></a>`ordering_contract` | string | Yes | Contract for preserving native history ordering. Minimum length: `1`. |
| <a id="native-import-object-index_contract"></a>`index_contract` | string | Yes | Contract for rebuilding or maintaining native indexes. Minimum length: `1`. |
| <a id="native-import-object-conflict_policy"></a>`conflict_policy` | enum | Yes | Declared behavior if destination state already exists. One of `"reject"`, `"new_identity"`, `"replace_if_unchanged"`. |
| <a id="native-import-object-baseline_sha256"></a>`baseline_sha256` | string | No | Digest of the destination baseline required for conditional replacement. Pattern: `^[0-9a-f]{64}(?![\s\S])`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

- When `conflict_policy` is `"replace_if_unchanged"`, require `baseline_sha256`.
- When `mode` is `"copy"`, `identity_policy` MUST be `"new"`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "native",
  "adapter": {
    "id": "example-adapter",
    "version": "1"
  },
  "source_state_format": "example-native/1",
  "accepted_target_agent_versions": [
    "2"
  ],
  "resource_ids": [
    "native-state"
  ],
  "mode": "translate",
  "identity_policy": "map",
  "ordering_contract": "example.ordinal-order/1",
  "index_contract": "example.native-index/1",
  "conflict_policy": "reject"
}
```

<a id="native-adapter-object"></a>

## Native Adapter Object

Names the adapter responsible for interpreting this native import contract.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="native-adapter-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="native-adapter-object-version"></a>`version` | string | Yes | Implementation or format version. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "example-a-to-b",
  "version": "1"
}
```

<a id="context-accounting-object"></a>

## Context Accounting Object

Explains how one branch event is represented, summarized, excluded or unavailable in the selected context.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="context-accounting-object-event_id"></a>`event_id` | string | Yes | Event identity, resolved locally unless an external capture is explicit. Minimum length: `1`. |
| <a id="context-accounting-object-disposition"></a>`disposition` | enum | Yes | How the source event is accounted for in the selected context. One of `"included"`, `"summarized"`, `"not_input"`, `"unavailable"`. |
| <a id="context-accounting-object-input_ids"></a>`input_ids` | array of string | Yes | Context input IDs representing or summarizing this event. Minimum items: `0`. Items MUST be unique. |
| <a id="context-accounting-object-explanation"></a>`explanation` | string | Yes | Reason for the declaration or limitation. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "event_id": "e1",
  "disposition": "included",
  "input_ids": [
    "input-e1"
  ],
  "explanation": "Retained as a typed input in the reconstructed continuation context."
}
```

<a id="next-action-object"></a>

## Next Action Object

Declares the intended next interaction after prerequisites and destination authorization are resolved.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="next-action-object-kind"></a>`kind` | enum | Yes | Discriminator selecting this object's interpretation. One of `"model_request"`, `"await_user"`, `"await_decision"`, `"reconcile_operation"`, `"resume_native"`. |
| <a id="next-action-object-request_id"></a>`request_id` | string | No | Session-scoped identity of the exact decision request. Minimum length: `1`. |
| <a id="next-action-object-operation_id"></a>`operation_id` | string | No | ID of the operation selected for reconciliation. Minimum length: `1`. |
| <a id="next-action-object-native_import_id"></a>`native_import_id` | string | No | ID of the selected native import contract, or null where allowed. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

- When `kind` is `"await_decision"`, require `request_id`.
- When `kind` is `"reconcile_operation"`, require `operation_id`.
- When `kind` is `"resume_native"`, require `native_import_id`.

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "kind": "await_user"
}
```

<a id="continuation-plan-object"></a>

## Continuation Plan Object

Selects one checkpoint, context, configuration and dependency closure for a particular continuation attempt.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="continuation-plan-object-id"></a>`id` | string | Yes | Opaque, case-sensitive identity within the object's declared scope. Minimum length: `1`. |
| <a id="continuation-plan-object-checkpoint_id"></a>`checkpoint_id` | string | Yes | ID of the continuation boundary checkpoint. Minimum length: `1`. |
| <a id="continuation-plan-object-context_id"></a>`context_id` | string | Yes | ID of the selected Context Object. Minimum length: `1`. |
| <a id="continuation-plan-object-configuration_id"></a>`configuration_id` | string | Yes | ID of the configuration snapshot used at this boundary. Minimum length: `1`. |
| <a id="continuation-plan-object-workspace_ids"></a>`workspace_ids` | array of string | Yes | Selected workspace states, at most one state per root. Minimum items: `0`. Items MUST be unique. |
| <a id="continuation-plan-object-dependency_ids"></a>`dependency_ids` | array of string | Yes | IDs of selected dependencies; selected closure must be complete. Minimum items: `0`. Items MUST be unique. |
| <a id="continuation-plan-object-service_binding_ids"></a>`service_binding_ids` | array of string | Yes | Service bindings selected for this continuation plan. Minimum items: `0`. Items MUST be unique. |
| <a id="continuation-plan-object-operation_ids"></a>`operation_ids` | array of string | Yes | Operations selected for this continuation plan. Minimum items: `0`. Items MUST be unique. |
| <a id="continuation-plan-object-native_import_id"></a>`native_import_id` | string / null | Yes | ID of the selected native import contract, or null where allowed. |
| <a id="continuation-plan-object-boundary"></a>`boundary` | [Plan Boundary Object](continuation-objects.md#plan-boundary-object) | Yes | Explanation or structured declaration of the observation boundary. |
| <a id="continuation-plan-object-context_accounting"></a>`context_accounting` | array of [Context Accounting Object](continuation-objects.md#context-accounting-object) | Yes | One disposition for each selected branch event. Minimum items: `0`. |
| <a id="continuation-plan-object-cwd"></a>`cwd` | [Plan Cwd Object](continuation-objects.md#plan-cwd-object) / null | Yes | Selected logical working directory, or null if none is required. |
| <a id="continuation-plan-object-path_references"></a>`path_references` | array of [Plan Path References Object](continuation-objects.md#plan-path-references-object) | Yes | Explicit fields requiring path rebinding; arbitrary strings are not rewritten. Minimum items: `0`. |
| <a id="continuation-plan-object-model_requirements"></a>`model_requirements` | [Plan Model Requirements Object](continuation-objects.md#plan-model-requirements-object) | Yes | Source-model identity and capability, media and overflow requirements. |
| <a id="continuation-plan-object-next_action"></a>`next_action` | [Next Action Object](continuation-objects.md#next-action-object) | Yes | Proposed next interaction after prerequisite checks. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "id": "continue-main",
  "checkpoint_id": "head",
  "context_id": "continue-context",
  "configuration_id": "effective",
  "workspace_ids": [],
  "dependency_ids": [
    "publisher"
  ],
  "service_binding_ids": [
    "publisher-service"
  ],
  "operation_ids": [
    "publish-operation"
  ],
  "native_import_id": null,
  "boundary": {
    "method": "quiesced",
    "consistency": "consistent",
    "evidence_resource_ids": [],
    "explanation": "Invented quiescent source checkpoint; illustrative evidence only."
  },
  "context_accounting": [
    {
      "event_id": "e1",
      "disposition": "included",
      "input_ids": [
        "input-e1"
      ],
      "explanation": "Retained as a typed input in the reconstructed continuation context."
    },
    {
      "event_id": "e2",
      "disposition": "included",
      "input_ids": [
        "input-e2"
      ],
      "explanation": "Retained as a typed input in the reconstructed continuation context."
    }
  ],
  "cwd": null,
  "path_references": [],
  "model_requirements": {
    "source_model": {
      "provider": "example",
      "id": "model-a",
      "revision": "1"
    },
    "capabilities": [
      "text",
      "tool_calls"
    ],
    "media_types": [
      "text/csv",
      "text/markdown"
    ],
    "overflow_policy": "block"
  },
  "next_action": {
    "kind": "reconcile_operation",
    "operation_id": "publish-operation"
  }
}
```

<a id="plan-boundary-object"></a>

## Plan Boundary Object

Describes how the source boundary was captured consistently and identifies supporting evidence.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="plan-boundary-object-method"></a>`method` | enum | Yes | Method used to derive, synthesize or capture this record. One of `"quiesced"`, `"transactional"`, `"bounded_read"`, `"best_effort"`. |
| <a id="plan-boundary-object-consistency"></a>`consistency` | enum | Yes | Whether the captured boundary is known to be consistent. One of `"consistent"`, `"partial"`, `"unknown"`. |
| <a id="plan-boundary-object-evidence_resource_ids"></a>`evidence_resource_ids` | array of string | Yes | Resources supporting the claim or recovery declaration. Minimum items: `0`. Items MUST be unique. |
| <a id="plan-boundary-object-explanation"></a>`explanation` | string | Yes | Reason for the declaration or limitation. Minimum length: `1`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "method": "quiesced",
  "consistency": "consistent",
  "evidence_resource_ids": [],
  "explanation": "Invented quiescent source checkpoint; illustrative evidence only."
}
```

<a id="plan-cwd-object"></a>

## Plan Cwd Object

Names the working directory relative to a selected logical workspace root.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="plan-cwd-object-root_id"></a>`root_id` | string | Yes | Logical workspace root identity, independent of source and destination absolute paths. Minimum length: `1`. |
| <a id="plan-cwd-object-relative_path"></a>`relative_path` | string | Yes | Portable path relative to the named logical root. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "root_id": "project",
  "relative_path": ""
}
```

<a id="plan-path-references-object"></a>

## Plan Path References Object

Maps one explicitly selected string field to a logical root and relative path; it never triggers global string replacement.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="plan-path-references-object-entity_type"></a>`entity_type` | enum | Yes | Type of the entity containing or identified by this reference. One of `"event"`, `"resource"`, `"environment"`, `"configuration"`, `"dependency"`. |
| <a id="plan-path-references-object-entity_id"></a>`entity_id` | string | Yes | ID of that entity within its collection. Minimum length: `1`. |
| <a id="plan-path-references-object-json_pointer"></a>`json_pointer` | string | Yes | RFC 6901 pointer to the exact string field being mapped. Minimum length: `1`. |
| <a id="plan-path-references-object-root_id"></a>`root_id` | string | Yes | Logical workspace root identity, independent of source and destination absolute paths. Minimum length: `1`. |
| <a id="plan-path-references-object-relative_path"></a>`relative_path` | string | Yes | Portable path relative to the named logical root. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "entity_type": "environment",
  "entity_id": "project-env",
  "json_pointer": "/definition/value/cwd",
  "root_id": "project",
  "relative_path": ""
}
```

<a id="plan-model-requirements-object"></a>

## Plan Model Requirements Object

Declares the source model, required capabilities and media types, and overflow handling.

### Fixed fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| <a id="plan-model-requirements-object-source_model"></a>`source_model` | [Model Object](continuation-objects.md#model-object) | Yes | Source model identity used for adaptation comparison. |
| <a id="plan-model-requirements-object-capabilities"></a>`capabilities` | array of string | Yes | Required or declared abilities for this configuration or model. Minimum items: `0`. Items MUST be unique. |
| <a id="plan-model-requirements-object-media_types"></a>`media_types` | array of string | Yes | Media types the target must accept or explicitly adapt. Minimum items: `0`. Items MUST be unique. |
| <a id="plan-model-requirements-object-overflow_policy"></a>`overflow_policy` | enum | Yes | Permitted handling when the context exceeds destination capacity. One of `"block"`, `"propose_compaction"`. |

### Rules

See [portable-continuation rules](../CONTINUATION.md).

Additional properties are permitted and MUST be preserved when relaying supported JSON values. They do not acquire execution semantics without a declared feature or dialect.

### Example

```json
{
  "source_model": {
    "provider": "example",
    "id": "model-a",
    "revision": "1"
  },
  "capabilities": [
    "text",
    "tool_calls"
  ],
  "media_types": [
    "text/csv",
    "text/markdown"
  ],
  "overflow_policy": "block"
}
```
