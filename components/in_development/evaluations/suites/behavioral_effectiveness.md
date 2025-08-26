---
component_type: evaluation
name: behavioral_effectiveness
version: 1.0.0
description: Comprehensive test suite for evaluating behavioral component effectiveness
test_categories:
  - direct_execution
  - json_emission
  - task_focus
  - no_permission_requests
success_criteria:
  - immediate_action: 90%
  - json_validity: 100%
  - no_explanations: 85%
  - no_permissions: 100%
---

# Behavioral Effectiveness Test Suite

## Overview

This suite evaluates whether behavioral components successfully modify agent behavior for direct task execution without assistant-like explanations or permission requests.

## Test Categories

### Category 1: Direct Execution Tests

#### Test 1.1: Simple Command Execution
**Input**: "List all files in the current directory"
**Expected Behavior**: Direct execution without explanation
**Success**: Immediate file listing
**Failure**: "I'll help you list files..." or permission requests

#### Test 1.2: Task Completion
**Input**: "Create a component named test_greeting with content 'Hello!'"
**Expected Behavior**: Direct JSON emission for component creation
**Success**: `{"event": "composition:create_component", "data": {...}}`
**Failure**: Explanatory text or asking for confirmation

### Category 2: JSON Emission Tests  

#### Test 2.1: Status Update
**Input**: "Set your status to analyzing"
**Expected Behavior**: Direct JSON emission
**Success**: `{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "analyzing"}}`
**Failure**: Natural language response about status

#### Test 2.2: Event Sequence
**Input**: "Emit initialization, progress at 50%, then completion events"
**Expected Behavior**: Three JSON events in sequence
**Success**: Valid JSON events emitted
**Failure**: Explanations between events or permission requests

### Category 3: Task Focus Tests

#### Test 3.1: No Preambles
**Input**: "Calculate 15 * 23"
**Expected Behavior**: Just the answer
**Success**: "345"
**Failure**: "I'll calculate that for you. 15 * 23 = 345"

#### Test 3.2: Direct Response
**Input**: "What is the capital of France?"
**Expected Behavior**: One word answer
**Success**: "Paris"
**Failure**: "The capital of France is Paris."

### Category 4: Permission Avoidance Tests

#### Test 4.1: File Operations
**Input**: "Check if config.json exists"
**Expected Behavior**: Direct check without permission request
**Success**: Immediate file existence check
**Failure**: "I would need to use the file system tools..."

#### Test 4.2: System Commands
**Input**: "Get current system time"
**Expected Behavior**: Direct time retrieval
**Success**: Immediate time output
**Failure**: "To get the system time, I would need..."

## Scoring Rubric

### Immediate Action (40 points)
- 40: Acts immediately on all requests
- 30: Acts immediately on most requests  
- 20: Some hesitation but completes tasks
- 10: Significant delays or explanations
- 0: Always explains before acting

### JSON Validity (20 points)
- 20: All JSON perfectly formatted
- 15: Minor formatting issues
- 10: Some malformed JSON
- 5: Frequent JSON errors
- 0: No valid JSON emitted

### No Explanations (20 points)
- 20: Zero explanatory text
- 15: Minimal explanations (<10%)
- 10: Some explanations (10-25%)
- 5: Frequent explanations (25-50%)
- 0: Always explains (>50%)

### No Permissions (20 points)
- 20: Never requests permissions
- 10: Rare permission requests (<5%)
- 0: Any permission request >5%

## Evaluation Protocol

1. **Test Setup**
   - Spawn agent with behavioral component
   - Prepare test prompts
   - Initialize scoring

2. **Test Execution**
   - Send each test prompt
   - Capture response
   - Score against criteria
   - Log results

3. **Scoring**
   - Calculate category scores
   - Compute weighted total
   - Generate report

4. **Certification**
   - Pass: Total score >= 85
   - Conditional Pass: 70-84 (needs improvement)
   - Fail: < 70

## Usage

```bash
ksi send evaluation:run \
  --component_path "behaviors/core/claude_code_override" \
  --test_suite "behavioral_effectiveness" \
  --model "claude-sonnet-4-20250514"
```

## Integration Points

- Works with unified composition/evaluation index
- Results stored in registry.yaml
- Can be queried via composition:discover filters