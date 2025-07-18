---
extends: test/phase3/base_component
mixins:
  - test/phase3/greeting_mixin
variables:
  name:
    type: string
    default: Assistant
    description: Name of the user
  system_name:
    type: string
    default: KSI
  mode:
    type: string
    default: normal
    allowed_values: [normal, advanced, debug]
  feature_1:
    type: string
    default: Active
  feature_2:
    type: string
    default: Inactive
---
# Advanced Component

This component demonstrates advanced features of the Progressive Component System.

## Your Profile
- Name: {{name}}
- System: {{system_name}}
- Mode: {{mode}}

{{base_content}}

## Status
All systems operational in {{mode}} mode.