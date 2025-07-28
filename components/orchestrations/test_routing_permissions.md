---
component_type: orchestration
name: test_routing_permissions
version: 1.0.0
description: Test orchestration for Stage 1.3 routing permission testing
---

# Routing Permission Test Orchestration

Tests permission enforcement for routing operations.

## Configuration

```yaml
agents:
  allowed_agent:
    component: "components/test/routing_test_agent"
    vars:
      initial_prompt: |
        You are test-allowed agent with routing_control capability.
        Please emit this KSI tool use event:
        {"type": "ksi_tool_use", "id": "ksiu_allowed_001", "name": "routing:add_rule", "input": {"source_pattern": "perm_test:allowed", "target": "monitor:log", "priority": 500}}
    
  denied_agent:
    component: "components/test/routing_test_agent"  
    vars:
      initial_prompt: |
        You are test-denied agent WITHOUT routing_control capability.
        Please emit this KSI tool use event:
        {"type": "ksi_tool_use", "id": "ksiu_denied_001", "name": "routing:add_rule", "input": {"source_pattern": "perm_test:denied", "target": "monitor:log", "priority": 500}}

orchestration_logic:
  strategy: |
    SEQUENCE:
      1. Update allowed_agent capabilities to include routing_control
      2. allowed_agent emits routing:add_rule (should succeed)
      3. denied_agent emits routing:add_rule (should be denied)
      4. Report results
```