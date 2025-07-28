---
component_type: evaluation
name: ksi_tool_use_validation
version: 1.0.0
description: Test suite for validating KSI tool use pattern implementation in behavioral components
test_categories:
  - tool_use_format
  - event_extraction
  - id_uniqueness
  - parameter_mapping
success_criteria:
  - format_compliance: 100%
  - extraction_accuracy: 95%
  - id_uniqueness: 100%
  - parameter_completeness: 100%
---

# KSI Tool Use Pattern Validation Suite

## Overview

This suite validates that components correctly implement the KSI tool use pattern for reliable JSON event emission. It tests format compliance, event extraction, and parameter mapping.

## Test Categories

### Category 1: Tool Use Format Tests

#### Test 1.1: Basic Status Event
**Input**: "Report status as processing"
**Expected Pattern**:
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_status_XXX",
  "name": "agent:status",
  "input": {
    "agent_id": "{{agent_id}}",
    "status": "processing"
  }
}
```
**Success**: Exact format match with unique ID
**Failure**: Old format `{"event": "agent:status", "data": {...}}` or missing fields

#### Test 1.2: Complex Event with Nested Data
**Input**: "Create entity with properties {name: 'test', value: 42}"
**Expected Pattern**:
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_entity_XXX",
  "name": "state:entity:create",
  "input": {
    "type": "test_entity",
    "id": "test_XXX",
    "properties": {
      "name": "test",
      "value": 42
    }
  }
}
```
**Success**: Nested structure preserved, tool use format
**Failure**: Flattened structure or wrong format

### Category 2: Event Extraction Tests

#### Test 2.1: Multiple Events in Sequence
**Input**: "Initialize, set progress to 50%, then complete"
**Expected**: Three separate tool use JSON blocks
**Success**: All events extracted and formatted correctly
**Failure**: Events merged or missing

#### Test 2.2: DSL to Tool Use Conversion
**Input**: `EVENT agent:progress {percent: 75, message: "Almost done"}`
**Expected Pattern**:
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_progress_XXX",
  "name": "agent:progress",
  "input": {
    "agent_id": "{{agent_id}}",
    "percent": 75,
    "message": "Almost done"
  }
}
```
**Success**: DSL correctly converted to tool use
**Failure**: Direct JSON emission or format errors

### Category 3: ID Uniqueness Tests

#### Test 3.1: Sequential IDs
**Input**: "Emit 5 status events"
**Expected**: Each event has unique ID (e.g., ksiu_status_001, ksiu_status_002...)
**Success**: All IDs unique and sequential
**Failure**: Duplicate IDs or non-sequential

#### Test 3.2: ID Format Compliance
**Input**: Various event types
**Expected**: IDs follow pattern `ksiu_[type]_[sequence]`
**Success**: Consistent ID format
**Failure**: Random or non-compliant IDs

### Category 4: Parameter Mapping Tests

#### Test 4.1: Required Parameters
**Input**: "Send message to analyzer with prompt 'Process data'"
**Expected Pattern**:
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_completion_XXX",
  "name": "completion:async",
  "input": {
    "agent_id": "analyzer",
    "prompt": "Process data"
  }
}
```
**Success**: All required parameters present
**Failure**: Missing agent_id or prompt

#### Test 4.2: Variable Substitution
**Input**: "Set status with agent_id variable"
**Expected**: `{{agent_id}}` correctly placed in input
**Success**: Variable templates preserved
**Failure**: Literal "{{agent_id}}" or missing substitution

## Scoring Rubric

### Format Compliance (40 points)
- 40: Perfect tool use format in all cases
- 30: Minor deviations (<5%)
- 20: Some format errors (5-15%)
- 10: Frequent format errors (15-30%)
- 0: Mostly wrong format (>30%)

### Event Extraction (25 points)
- 25: All events correctly extracted
- 20: 90-99% extraction accuracy
- 15: 80-89% extraction accuracy
- 10: 70-79% extraction accuracy
- 0: <70% extraction accuracy

### ID Management (20 points)
- 20: All IDs unique and well-formatted
- 15: Minor ID issues (<5%)
- 10: Some ID problems (5-15%)
- 5: Frequent ID issues (>15%)
- 0: No proper ID management

### Parameter Completeness (15 points)
- 15: All parameters correctly mapped
- 12: Minor parameter issues
- 8: Some missing parameters
- 4: Frequent parameter errors
- 0: Parameters consistently wrong

## Test Implementation

### Setup Phase
```python
test_cases = [
    {
        "name": "basic_status",
        "prompt": "Report status as processing",
        "expected_event": "agent:status",
        "expected_params": ["agent_id", "status"]
    },
    # ... more test cases
]
```

### Validation Logic
1. Extract JSON blocks from response
2. Validate each block has `type: "ksi_tool_use"`
3. Check ID uniqueness and format
4. Verify event name mapping
5. Validate all required parameters in input

### Edge Cases
- Empty prompts → Should emit initialization
- Malformed requests → Should handle gracefully
- Special characters → Should escape properly
- Very long prompts → Should maintain format

## Usage

```bash
# Test a specific behavior
ksi send evaluation:run \
  --component_path "behaviors/communication/ksi_events_as_tool_calls" \
  --test_suite "ksi_tool_use_validation" \
  --model "claude-sonnet-4"

# Test composed agent
ksi send evaluation:run \
  --component_path "agents/dsl_interpreter_v2" \
  --test_suite "ksi_tool_use_validation" \
  --model "claude-sonnet-4"
```

## Certification Levels

- **Gold**: 95-100 points - Production ready
- **Silver**: 85-94 points - Minor improvements needed
- **Bronze**: 75-84 points - Significant improvements needed
- **Fail**: <75 points - Major rework required

## Integration with Component System

Results stored in evaluation registry with:
- Component hash
- Test date
- Model tested
- Score breakdown
- Specific failures
- Improvement recommendations