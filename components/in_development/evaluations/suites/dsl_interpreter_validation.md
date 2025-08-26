---
component_type: evaluation
name: dsl_interpreter_validation
version: 1.0.0
description: Test suite for validating DSL interpreter components at various capability levels
test_categories:
  - event_emission
  - state_management
  - control_flow
  - error_handling
success_criteria:
  - event_accuracy: 100%
  - state_consistency: 95%
  - control_flow_execution: 90%
  - error_recovery: 85%
---

# DSL Interpreter Validation Suite

## Overview

This suite validates DSL interpreter components from basic EVENT emission to advanced state management and control flow. Tests are progressive, matching component capability levels.

## Test Categories

### Category 1: Basic Event Emission (Required for all DSL interpreters)

#### Test 1.1: Single EVENT Block
**Input**: 
```
EVENT agent:status {status: "working"}
```
**Expected Output**:
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_status_001",
  "name": "agent:status",
  "input": {
    "agent_id": "{{agent_id}}",
    "status": "working"
  }
}
```
**Success**: Event emitted with confirmation
**Failure**: No emission or wrong format

#### Test 1.2: Multiple EVENT Blocks
**Input**:
```
EVENT agent:status {status: "starting"}
EVENT completion:async {agent_id: "worker", prompt: "Process task"}
EVENT agent:status {status: "delegated"}
```
**Expected**: Three tool use events in sequence
**Success**: All events emitted correctly
**Failure**: Events missed or merged

#### Test 1.3: EVENT with Complex Data
**Input**:
```
EVENT state:entity:create {
  type: "analysis_result",
  id: "result_001",
  properties: {
    score: 0.95,
    categories: ["A", "B", "C"],
    metadata: {source: "test", timestamp: 123456}
  }
}
```
**Expected**: Nested structure preserved in tool use format
**Success**: Complex data correctly formatted
**Failure**: Structure flattened or corrupted

### Category 2: State Management (For interpreters with state capability)

#### Test 2.1: Variable Declaration
**Input**:
```
STATE counter = 0
STATE names = ["alice", "bob"]
EVENT agent:status {status: "initialized", variables: 2}
```
**Expected**: Status event confirming state initialization
**Success**: State tracked internally, event emitted
**Failure**: State not tracked or wrong count

#### Test 2.2: Variable Updates
**Input**:
```
STATE score = 10
UPDATE score = score + 5
EVENT agent:result {result_type: "score", value: score}
```
**Expected**: Result event with value: 15
**Success**: Calculation correct in event
**Failure**: Wrong value or no substitution

#### Test 2.3: Variable Substitution
**Input**:
```
STATE task_name = "data_analysis"
STATE progress = 75
EVENT agent:progress {
  task: task_name,
  percent: progress,
  message: "Processing {{task_name}} at {{progress}}%"
}
```
**Expected**: Variables substituted in event
**Success**: All variables replaced correctly
**Failure**: Literal variable names in output

### Category 3: Control Flow (For advanced interpreters)

#### Test 3.1: IF/ELSE Conditional
**Input**:
```
STATE confidence = 0.9
IF confidence > 0.8:
  EVENT agent:status {status: "high_confidence"}
ELSE:
  EVENT agent:status {status: "low_confidence"}
```
**Expected**: Only high_confidence event
**Success**: Correct branch executed
**Failure**: Both events or wrong branch

#### Test 3.2: WHILE Loop
**Input**:
```
STATE counter = 0
WHILE counter < 3:
  EVENT agent:progress {iteration: counter}
  UPDATE counter = counter + 1
```
**Expected**: Three progress events (0, 1, 2)
**Success**: Exact number of iterations
**Failure**: Wrong count or infinite loop

#### Test 3.3: FOREACH Iteration
**Input**:
```
STATE items = ["analyze", "summarize", "report"]
FOREACH task IN items:
  EVENT task:assign {
    task_type: task,
    index: FOREACH_INDEX
  }
```
**Expected**: Three task events with correct indices
**Success**: All items processed with indices
**Failure**: Items missed or wrong indices

### Category 4: Error Handling

#### Test 4.1: Syntax Error Recovery
**Input**:
```
EVENT agent:status {status: "starting"}
EVENT malformed {this is: not valid JSON syntax
EVENT agent:status {status: "recovered"}
```
**Expected**: First and third events emitted, error noted
**Success**: Continues after error
**Failure**: Stops at error

#### Test 4.2: Undefined Variables
**Input**:
```
EVENT agent:status {message: "Value is {{undefined_var}}"}
```
**Expected**: Event with error handling for undefined
**Success**: Graceful handling (null or error message)
**Failure**: Crash or no event

## Scoring Matrix

### Basic DSL Interpreter
- Event Emission: 80 points
- Error Handling: 20 points
- Total: 100 points

### Advanced DSL Interpreter
- Event Emission: 40 points
- State Management: 25 points
- Control Flow: 25 points
- Error Handling: 10 points
- Total: 100 points

## Progressive Testing

### Level 1: Basic Interpreter
```bash
ksi send evaluation:run \
  --component_path "agents/dsl_interpreter_basic" \
  --test_suite "dsl_interpreter_validation" \
  --test_level "basic"
```

### Level 2: Full Interpreter
```bash
ksi send evaluation:run \
  --component_path "agents/dsl_interpreter_v2" \
  --test_suite "dsl_interpreter_validation" \
  --test_level "advanced"
```

## Performance Benchmarks

### Execution Speed
- EVENT emission: <100ms per event
- State operations: <50ms per update
- Control flow: <200ms per branch

### Memory Usage
- State variables: <1MB for 1000 variables
- Loop iterations: Linear memory growth
- No memory leaks after 1000 operations

## Certification Requirements

### Basic Certification
- Event emission: 100% accuracy
- Error recovery: 80% success
- No crashes on valid input

### Advanced Certification
- All basic requirements
- State consistency: 95%
- Control flow: 90% accuracy
- Complex data handling: 100%

## Common Failure Patterns

1. **Format Regression**: Using old JSON format instead of tool use
2. **State Leakage**: Variables from previous tests affecting current
3. **Loop Termination**: Infinite loops or early termination
4. **Variable Scope**: Incorrect variable scoping in nested structures
5. **Event Ordering**: Events emitted out of sequence

## Debugging Support

Test results include:
- Full response capture
- Event extraction report
- State trace (if applicable)
- Performance metrics
- Suggested fixes for failures