name: test_parent_orchestrator
component_type: orchestration
version: 1.0.0
description: Parent orchestration that spawns child orchestrations
author: test_system

event_propagation:
  subscription_level: -1  # Receive ALL events from entire tree
  error_handling: bubble

agents:
  orchestrator:
    component: components/core/system_orchestrator
    capabilities: [orchestration]
    vars:
      agent_id: "parent_orchestrator"

initialization:
  strategy: broadcast
  message: |
    You are a parent orchestrator. Your task is to demonstrate nested orchestrations.
    
    Spawn a child orchestration using this event:
    {"event": "orchestration:start", "data": {"pattern": "orchestrations/hello_goodbye", "vars": {"parent_orchestration_id": "{{orchestration_id}}"}}}