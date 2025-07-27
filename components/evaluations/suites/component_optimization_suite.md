---
component_type: evaluation
name: component_optimization_suite
version: 1.0.0
description: Comprehensive evaluation suite for optimized components combining multiple metrics
evaluation_type: suite
dependencies:
  - evaluations/metrics/clarity_score_metric
  - evaluations/metrics/effectiveness_judge
---

# Component Optimization Evaluation Suite

A comprehensive evaluation framework for assessing optimized KSI components using both programmatic metrics and LLM-as-Judge evaluations.

## Suite Components

### 1. Programmatic Metrics
- **Clarity Score**: Structural analysis of component organization
- **JSON Emission Rate**: For components that should emit KSI events
- **Instruction Specificity**: Measurable actionability of instructions
- **Component Completeness**: Presence of required elements

### 2. LLM-as-Judge Evaluations
- **Effectiveness Judge**: Pairwise comparison of component quality
- **Domain Expertise Judge**: Assessment of role-appropriate knowledge
- **Innovation Judge**: Evaluation of creative approaches

### 3. Behavioral Testing
- **Spawn Test**: Can the component be successfully spawned as an agent?
- **Event Emission Test**: Does the agent emit expected events?
- **Task Completion Test**: Can the agent complete basic tasks?

## Evaluation Process

### Phase 1: Static Analysis
```python
def evaluate_static(component_content: str) -> dict:
    """Run all programmatic metrics on component content."""
    return {
        "clarity_score": clarity_score(component_content),
        "json_emission_potential": analyze_json_patterns(component_content),
        "instruction_specificity": measure_specificity(component_content),
        "completeness": check_required_elements(component_content)
    }
```

### Phase 2: Comparative Evaluation
For optimization assessment, compare original vs optimized:
1. Run static analysis on both versions
2. Use LLM judges for pairwise comparison
3. Calculate improvement metrics

### Phase 3: Behavioral Validation
```bash
# Test agent spawn and basic functionality
ksi send agent:spawn --component "optimized_component_path"
# Monitor for expected events
ksi send monitor:get_events --agent-id "spawned_agent_id"
```

## Scoring Framework

### Overall Score Calculation
```
overall_score = (
    static_weight * static_score +
    judge_weight * judge_score +
    behavioral_weight * behavioral_score
)

where:
- static_weight = 0.3
- judge_weight = 0.5
- behavioral_weight = 0.2
```

### Improvement Metrics
```
improvement_ratio = optimized_score / original_score
effectiveness_gain = judge_preference_rate
behavioral_success_rate = passed_tests / total_tests
```

## Usage in Optimization Pipeline

### Integration with DSPy/MIPROv2
1. Use static metrics as fast evaluation during optimization
2. Apply judge evaluation for final candidate selection
3. Validate winning candidates with behavioral tests

### Example Workflow
```yaml
optimization_evaluation:
  pre_optimization:
    - measure: baseline_static_scores
    - record: original_component_hash
  
  during_optimization:
    - metric: clarity_score  # Fast feedback
    - threshold: 0.6  # Minimum acceptable
  
  post_optimization:
    - compare: original vs optimized
    - judge: effectiveness_comparison
    - test: behavioral_validation
    - decision: accept if improvement_ratio > 1.2
```

## Quality Gates

### Minimum Standards
- Clarity score ≥ 0.6
- At least one successful behavioral test
- Judge preference over original ≥ 60%

### Excellence Criteria
- Clarity score ≥ 0.85
- All behavioral tests pass
- Judge preference ≥ 80%
- Demonstrates innovation

## Reporting

### Evaluation Report Structure
```json
{
  "component": "component_path",
  "version": "optimized_v1",
  "scores": {
    "static": 0.78,
    "judge": 0.85,
    "behavioral": 1.0,
    "overall": 0.84
  },
  "improvement": {
    "ratio": 1.35,
    "key_gains": ["clarity", "specificity"],
    "behavioral_changes": ["now emits JSON correctly"]
  },
  "recommendation": "Accept optimization - significant improvements"
}
```

## Suite Configuration

### For Persona Components
- Weight clarity and domain expertise higher
- Test conversation continuity
- Evaluate role-specific capabilities

### For Orchestration Components
- Focus on coordination patterns
- Test multi-agent scenarios
- Evaluate emergent behaviors

### For Tool Components
- Emphasize reliability and error handling
- Test edge cases
- Validate integration points