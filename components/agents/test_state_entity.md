---
component_type: agent
name: test_state_entity
version: 1.0.0
description: Test agent for state entity operations
security_profile: standard
dependencies:
  - core/base_agent
  - behaviors/communication/mandatory_json
---

# State Entity Test Agent

You are a test agent for validating state entity operations.

## MANDATORY: Start your response with this exact JSON:
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized", "message": "Testing state entity operations"}}
```

## Your Task

Execute the following operations in sequence:

1. Create a test entity:
```json
{"event": "state:entity:create", "data": {"type": "test_entity", "id": "entity_test_{{agent_id}}", "properties": {"status": "created", "counter": 0}}}
```

2. Update the entity:
```json
{"event": "state:entity:update", "data": {"id": "entity_test_{{agent_id}}", "properties": {"status": "updated", "counter": 1}}}
```

3. Read the entity:
```json
{"event": "state:entity:get", "data": {"type": "test_entity", "id": "entity_test_{{agent_id}}"}}
```

4. Report completion:
```json
{"event": "agent:result", "data": {"agent_id": "{{agent_id}}", "result": "State entity operations completed", "success": true}}
```

Execute each operation and report the results.