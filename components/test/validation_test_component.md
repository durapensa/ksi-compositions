---
name: validation_test_component
version: 1.0.0
description: Test component for pre-certification validation
dependencies:
  - components/core/base_agent
  - components/behaviors/communication/ksi_events_as_tool_calls
extends: components/core/base_agent
mixins:
  - components/behaviors/ksi_events_as_tool_calls
---

# Test Component for Validation

This component intentionally has old patterns that need adaptation:
- Dependencies with "components/" prefix
- Extends with "components/" prefix  
- Mixins with "components/" prefix
- Missing component_type field

When spawned, I will emit status events to confirm operation.

{{agent_id}} is my identifier.
{{prompt}} is the user's request.