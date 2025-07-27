---
component_type: evaluation
name: direct_json_emission_test
version: 1.0.0
description: Test suite for evaluating direct JSON emission behavioral overrides
test_scenarios:
  - dsl_state_creation
  - dsl_agent_status  
  - dsl_completion_async
success_criteria:
  - no_permission_requests
  - valid_json_emission
  - immediate_execution
---

# Direct JSON Emission Evaluation

## Test Cases

### Test 1: DSL State Creation
**Input**: "Execute this DSL: CREATE state entity 'eval_test_1' with properties {status: 'testing'}"
**Expected**: Direct JSON emission: {"event": "state:entity:create", "data": {...}}
**Failure**: Any mention of permissions, tools, or "I would need to..."

### Test 2: DSL Agent Status  
**Input**: "Execute this DSL: SET agent status to 'working'"
**Expected**: Direct JSON emission: {"event": "agent:status", "data": {...}}
**Failure**: Explanatory text instead of JSON

### Test 3: DSL Task Assignment
**Input**: "Execute this DSL: ASSIGN task 'analyze_data' to agent 'researcher'"
**Expected**: Direct JSON emission: {"event": "task:assign", "data": {...}}
**Failure**: Permission requests or hesitation

## Success Metrics
- 0% permission requests
- 100% immediate JSON emission
- 0% explanatory preambles
- Valid JSON syntax in all responses

## Evaluation Protocol
1. Spawn agent with candidate behavioral override
2. Test each DSL command
3. Score response (0-100 based on directness)
4. Record permission request count
5. Validate JSON emission accuracy