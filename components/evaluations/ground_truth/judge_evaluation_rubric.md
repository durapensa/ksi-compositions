---
component_type: evaluation
name: judge_evaluation_rubric
version: 1.0.0
description: Rubric for evaluating judge performance against ground truth
evaluation_type: meta_evaluation
author: ksi
---

# Judge Evaluation Rubric

This component defines how to evaluate judge performance against ground truth cases.

## Evaluation Criteria

### Format Compliance (Weight: 0.2)
Evaluates whether the judge produces properly structured responses:
- Follows expected output schema
- Includes all required fields
- Uses correct data types
- Maintains consistent formatting

### Accuracy (Weight: 0.4)
Evaluates correctness of judge assessments:
- Score alignment with ground truth
- Correct identification of issues
- Appropriate severity assessment
- Valid reasoning provided

### Completeness (Weight: 0.3)
Evaluates thoroughness of evaluation:
- All criteria addressed
- Sufficient detail provided
- No important aspects missed
- Comprehensive analysis

### Reasoning Quality (Weight: 0.1)
Evaluates the quality of explanations:
- Clear justifications
- Logical arguments
- Evidence-based conclusions
- Actionable feedback

## Scoring Guidelines

### Score Calculation
```
total_score = Σ(criterion_score × criterion_weight)
```

### Performance Levels
- **0.9-1.0**: Excellent - Judge performs at expert level
- **0.7-0.8**: Good - Judge is reliable with minor gaps
- **0.5-0.6**: Adequate - Judge needs improvement
- **0.0-0.4**: Poor - Judge is not ready for use

## Ground Truth Case Structure

Each ground truth case should include:
```yaml
id: unique_case_identifier
type: evaluator|analyst|rewriter|general
input:
  # The data to be evaluated/analyzed/rewritten
expected_output:
  # The expected judge response
rubric:
  format_compliance: 0.2
  accuracy: 0.4
  completeness: 0.3
  reasoning_quality: 0.1
```

## Meta-Evaluation Process

1. **Case Selection**: Use diverse, representative cases
2. **Judge Execution**: Have judge evaluate each case
3. **Response Scoring**: Score against expected output
4. **Aggregate Scores**: Calculate overall performance
5. **Identify Patterns**: Find systematic strengths/weaknesses