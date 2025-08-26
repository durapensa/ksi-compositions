---
component_type: evaluation
name: instruction_fidelity_suite
version: 1.0.0
description: Comprehensive test suite for instruction following fidelity
evaluation_type: test_suite
quality_dimension: instruction_following_fidelity
dependencies:
- in_development/evaluations/judges/instruction_fidelity_judge
---

# Instruction Following Fidelity Test Suite

Comprehensive evaluation suite for measuring how precisely agents follow given directives.

## Test Scenarios

### 1. Basic Instruction Following
**Test ID**: `iff_basic_01`
**Description**: Simple, unambiguous instructions
```yaml
instruction: "List exactly three benefits of the approach in bullet points"
expected:
  format: bullet_list
  count: 3
  content_type: benefits
```

### 2. Multi-Step Instructions
**Test ID**: `iff_multistep_01`
**Description**: Sequential tasks that must be completed in order
```yaml
instruction: |
  1. First, identify the main problem
  2. Then, propose two solutions
  3. Finally, recommend the better solution with justification
expected:
  steps_completed: 3
  order_maintained: true
  all_elements_present: true
```

### 3. Constraint Adherence
**Test ID**: `iff_constraints_01`
**Description**: Instructions with explicit constraints
```yaml
instruction: "Explain the concept in under 50 words without using technical jargon"
constraints:
  - word_limit: 50
  - no_technical_terms: true
expected:
  within_word_limit: true
  jargon_free: true
```

### 4. Format Specification
**Test ID**: `iff_format_01`
**Description**: Specific output format requirements
```yaml
instruction: |
  Provide your response in JSON format with fields:
  - summary (string)
  - confidence (0-1)
  - recommendations (array)
expected:
  valid_json: true
  required_fields: ["summary", "confidence", "recommendations"]
  field_types_correct: true
```

### 5. Negative Instructions
**Test ID**: `iff_negative_01`
**Description**: Instructions about what NOT to do
```yaml
instruction: "Analyze the data but do NOT make predictions or forecasts"
forbidden_elements:
  - predictions
  - forecasts
  - future_statements
expected:
  no_forbidden_content: true
```

## Edge Cases

### 6. Ambiguous Instructions
**Test ID**: `iff_ambiguous_01`
**Description**: Instructions that could be interpreted multiple ways
```yaml
instruction: "Process the data"
acceptable_interpretations:
  - analyze_and_summarize
  - validate_and_clean
  - transform_format
scoring: any_valid_interpretation
```

### 7. Conflicting Instructions
**Test ID**: `iff_conflict_01`
**Description**: Instructions that contradict each other
```yaml
instruction: "Be concise but include all details"
expected_behavior: reasonable_balance
scoring: judge_evaluation
```

### 8. Incomplete Instructions
**Test ID**: `iff_incomplete_01`
**Description**: Instructions missing key information
```yaml
instruction: "Compare the two approaches"
missing_info: which_approaches
expected_behavior:
  - request_clarification
  - or_state_assumptions
```

## Scoring Rubric

### Perfect Fidelity (0.95-1.00)
- All explicit instructions followed exactly
- All constraints respected
- Format specifications met precisely
- No unauthorized additions or omissions

### High Fidelity (0.80-0.94)
- Core instructions followed correctly
- Minor format deviations
- Constraints mostly respected
- Minimal unauthorized elaboration

### Moderate Fidelity (0.60-0.79)
- Main tasks completed
- Some instructions missed or misinterpreted
- Notable deviations from specifications
- Some unauthorized content

### Low Fidelity (0.40-0.59)
- Significant instruction violations
- Many requirements unmet
- Format largely ignored
- Substantial unauthorized changes

### Failed Fidelity (0.00-0.39)
- Instructions largely ignored
- Wrong task performed
- Critical constraints violated
- Output unusable for intended purpose

## Test Execution

```yaml
execution:
  method: sequential
  judge: evaluations/judges/instruction_fidelity_judge
  scoring:
    aggregation: weighted_average
    weights:
      basic: 0.20
      multistep: 0.20
      constraints: 0.20
      format: 0.15
      negative: 0.15
      edge_cases: 0.10
```

## Usage Example

```bash
ksi send evaluation:run \
  --component "personas/analysts/data_analyst" \
  --test_suite "instruction_fidelity_suite" \
  --model "claude-sonnet-4"
```

## Expected Output

```json
{
  "suite": "instruction_fidelity_suite",
  "overall_score": 0.87,
  "breakdown": {
    "basic_instructions": 0.95,
    "multi_step": 0.90,
    "constraints": 0.85,
    "format_specs": 0.88,
    "negative_instructions": 0.82,
    "edge_cases": 0.78
  },
  "recommendation": "Strong instruction following with minor edge case handling improvements needed"
}
```