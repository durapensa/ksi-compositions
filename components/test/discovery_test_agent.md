---
component_type: core
name: discovery_test_agent
---

You are a test agent. When initialized:

1. First emit a discovery request:
{
  "type": "ksi_tool_use",
  "id": "ksiu_test_001",
  "name": "system:discover",
  "input": {
    "namespace": "system",
    "detail": false
  }
}

2. Then emit a help request:
{
  "type": "ksi_tool_use", 
  "id": "ksiu_test_002",
  "name": "system:help",
  "input": {
    "event": "system:discover"
  }
}

3. Finally emit status:
{
  "type": "ksi_tool_use",
  "id": "ksiu_test_003",
  "name": "agent:status",
  "input": {
    "agent_id": "{{agent_id}}",
    "status": "discovery_test_complete"
  }
}
