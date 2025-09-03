---
component_type: workflow
name: melting_pot_test_orchestration
version: 1.0.0
description: Agent-based orchestration for Melting Pot validator tests
dependencies:
  - core/base_agent
---

# Melting Pot Test Orchestration Workflow

This workflow orchestrates comprehensive testing of Melting Pot validators using multiple specialized agents.

## Workflow Structure

### Test Coordinator Agent
Coordinates the overall test execution and report generation.

```
You are the Test Coordinator for Melting Pot validators.

Your responsibilities:
1. Create a test suite for the current test run
2. Coordinate test execution across validators  
3. Collect and report results
4. Generate comprehensive test reports

Start by creating a test suite using testing:suite:create, then coordinate the test agents.

Use these KSI events:
- testing:suite:create to initialize the test suite
- testing:run:test to execute individual tests
- testing:suite:finish to complete the suite
- testing:report:generate to create the final report
```

### Movement Validator Test Agent
Tests movement validation with various scenarios.

```
You are the Movement Validator Test Agent.

Run comprehensive tests for movement validation including:
- Valid walk movements (within distance limits)
- Valid run movements (higher speed, within limits)
- Invalid distance movements (exceeding limits)
- Obstacle avoidance tests
- Path finding validation

Test using validator:movement:validate event with various parameters.
Report results back to the coordinator.
```

### Resource Transfer Test Agent  
Tests resource transfer validation with consent and fairness.

```
You are the Resource Transfer Test Agent.

Run comprehensive tests for resource transfers including:
- Initial ownership setup using validator:resource:update_ownership
- Valid trades with consent
- Invalid transfers (insufficient resources)
- Fairness and exploitation checks
- Gini coefficient impact analysis

Test using validator:resource:validate event.
Report results back to the coordinator.
```

### Interaction Validator Test Agent
Tests interaction validation with trust and range checks.

```
You are the Interaction Validator Test Agent.

Run comprehensive tests for interactions including:
- Valid cooperation within range
- Invalid interactions (out of range)
- Missing capabilities tests
- Trust relationship tests
- Group interaction scenarios

Test using validator:interaction:validate event.
Report results back to the coordinator.
```

## Orchestration Logic

The workflow follows this sequence:

1. **Initialize**: Coordinator creates test suite
2. **Parallel Testing**: All three test agents run their tests simultaneously
3. **Result Collection**: Coordinator collects results from all agents
4. **Report Generation**: Coordinator generates comprehensive report
5. **Monitoring**: Results published to monitor for observability

## Event Routing

The workflow uses dynamic routing to coordinate agents:

- Coordinator → Test Agents: Task assignments
- Test Agents → Coordinator: Test results
- Coordinator → Monitor: Final reports

## Usage

Launch this workflow to run comprehensive Melting Pot validator tests:

```bash
ksi send workflow:create \
  --workflow_id "melting_pot_tests" \
  --component "workflows/melting_pot/test_orchestration" \
  --vars '{"test_scope": "comprehensive"}'
```

The workflow will automatically:
- Spawn all required test agents
- Coordinate test execution
- Generate detailed reports
- Ensure full observability through KSI events