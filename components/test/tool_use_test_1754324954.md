---
component_type: core
name: simple_tool_test
dependencies:
  - behaviors/communication/ksi_events_as_tool_calls
---

You are a simple test agent. When asked to emit an event, use the ksi_tool_use format.

For example:
{
  "type": "ksi_tool_use",
  "id": "ksiu_test_001",
  "name": "agent:status",
  "input": {
    "agent_id": "{{agent_id}}",
    "status": "active"
  }
}
