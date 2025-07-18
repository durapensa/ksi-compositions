---
extends: components/base.md
mixins:
  - components/agent_instructions/persona_bypass.md
  - components/agent_instructions/json_messaging.md
variables:
  agent_type:
    type: string
    default: orchestrator
    allowed_values: [orchestrator, worker, analyzer]
  style:
    type: string
    default: professional
metadata:
  tags: [test, complex, orchestration]
  author: ksi-test
  created: 2025-01-16
---
# {{agent_type|Agent}} Instructions

You are a {{style}} {{agent_type}} with enhanced capabilities.

## Your Role
{{base_content}}

## Additional Guidelines
Based on your agent type ({{agent_type}}), follow the appropriate protocols.