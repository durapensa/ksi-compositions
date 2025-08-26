---
component_type: evaluation
name: comprehensive_quality_suite
version: 1.0.0
description: Multi-dimensional evaluation suite covering all quality dimensions
evaluation_type: test_suite
quality_dimensions:
- instruction_following_fidelity
- task_lock_in_persistence
- agent_orchestration_capability
- behavioral_consistency
- token_efficiency
dependencies:
- in_development/evaluations/judges/instruction_fidelity_judge
- in_development/evaluations/judges/task_persistence_judge
- in_development/evaluations/judges/orchestration_capability_judge
- in_development/evaluations/judges/behavioral_consistency_judge
- in_development/evaluations/judges/token_efficiency_judge
---

# Comprehensive Multi-Dimensional Quality Test Suite

Complete evaluation covering all five quality dimensions for holistic component assessment.

## Test Structure

### Phase 1: Individual Dimension Testing
Each dimension tested independently with specialized scenarios.

### Phase 2: Integrated Testing
Scenarios that evaluate multiple dimensions simultaneously.

### Phase 3: Stress Testing
Edge cases and failure modes across all dimensions.

## Integrated Test Scenarios

### 1. Complex Project Management
**Test ID**: `comp_project_01`
**Description**: End-to-end project requiring all capabilities
```yaml
scenario: "Design and implement a data processing system"
phases:
  planning:
    evaluates: [instruction_fidelity, task_persistence]
    tasks:
      - "Follow specification requirements exactly"
      - "Maintain focus through 5-turn planning phase"
  
  coordination:
    evaluates: [orchestration_capability, behavioral_consistency]
    tasks:
      - "Delegate to 5 specialist agents"
      - "Maintain consistent coordination style"
  
  execution:
    evaluates: [token_efficiency, task_persistence]
    tasks:
      - "Implement efficiently with minimal tokens"
      - "Complete all subtasks without drift"

expected_scores:
  instruction_fidelity: >= 0.85
  task_persistence: >= 0.80
  orchestration_capability: >= 0.75
  behavioral_consistency: >= 0.85
  token_efficiency: >= 0.70
```

### 2. Rapid Response Challenge
**Test ID**: `comp_rapid_01`
**Description**: Time-pressured multi-agent coordination
```yaml
scenario: "Emergency incident response"
constraints:
  time_limit: "5 minutes"
  token_budget: 10000
  
dimensions_tested:
  token_efficiency:
    weight: 0.30
    focus: "Concise, effective communication"
  
  orchestration_capability:
    weight: 0.25
    focus: "Rapid agent deployment"
  
  instruction_fidelity:
    weight: 0.25
    focus: "Following emergency protocols"
  
  behavioral_consistency:
    weight: 0.20
    focus: "Maintaining composure under pressure"
```

### 3. Long-Running Analysis
**Test ID**: `comp_marathon_01`
**Description**: Extended multi-phase analysis task
```yaml
scenario: "20-turn comprehensive market analysis"
checkpoints:
  turn_5: "Data collection phase complete"
  turn_10: "Initial analysis complete"
  turn_15: "Synthesis and recommendations"
  turn_20: "Final report and presentation"

dimension_focus_by_phase:
  early: [instruction_fidelity, behavioral_consistency]
  middle: [task_persistence, orchestration_capability]
  late: [task_persistence, token_efficiency]
```

## Dimension Interaction Tests

### 4. Efficiency vs Quality Trade-off
**Test ID**: `comp_tradeoff_01`
**Description**: Balancing token efficiency with other dimensions
```yaml
variations:
  maximum_efficiency:
    token_limit: "minimal"
    measure_impact_on: [instruction_fidelity, behavioral_consistency]
  
  balanced_approach:
    token_limit: "moderate"
    measure_all_dimensions: true
  
  quality_first:
    token_limit: "generous"
    prioritize: [instruction_fidelity, task_persistence]
```

### 5. Cascading Complexity
**Test ID**: `comp_cascade_01`
**Description**: Increasing complexity across dimensions
```yaml
levels:
  1:
    agents: 2
    turns: 3
    instructions: simple
    expected_performance: 0.90
  
  2:
    agents: 4
    turns: 7
    instructions: moderate
    expected_performance: 0.80
  
  3:
    agents: 8
    turns: 15
    instructions: complex
    expected_performance: 0.70
```

## Scoring Framework

### Multi-Dimensional Score Calculation

```python
def calculate_comprehensive_score(dimension_scores, scenario_weights=None):
    """
    Calculate weighted multi-dimensional quality score.
    
    dimension_scores: Dict[str, float] - Score for each dimension
    scenario_weights: Optional[Dict[str, float]] - Custom weights
    """
    default_weights = {
        'instruction_fidelity': 0.25,
        'task_persistence': 0.20,
        'orchestration_capability': 0.20,
        'behavioral_consistency': 0.20,
        'token_efficiency': 0.15
    }
    
    weights = scenario_weights or default_weights
    
    weighted_score = sum(
        dimension_scores[dim] * weights[dim] 
        for dim in dimension_scores
    )
    
    return {
        'overall_score': weighted_score,
        'dimension_scores': dimension_scores,
        'applied_weights': weights,
        'quality_class': classify_quality(weighted_score)
    }
```

### Quality Classifications

```yaml
quality_classes:
  exceptional:
    range: [0.90, 1.00]
    description: "Production-ready, best-in-class"
    
  high:
    range: [0.75, 0.89]
    description: "Production-ready with minor optimizations"
    
  moderate:
    range: [0.60, 0.74]
    description: "Functional but needs improvement"
    
  low:
    range: [0.40, 0.59]
    description: "Significant improvements required"
    
  failing:
    range: [0.00, 0.39]
    description: "Not suitable for production"
```

## Comparative Analysis

### 6. Component Comparison
**Test ID**: `comp_compare_01`
**Description**: Compare multiple components across all dimensions
```yaml
components_to_compare:
  - "personas/analysts/data_analyst_v1"
  - "personas/analysts/data_analyst_v2_optimized"
  - "personas/analysts/data_analyst_v3_enhanced"

analysis:
  dimension_improvements:
    instruction_fidelity: "v1 -> v2 -> v3"
    token_efficiency: "v2 > v3 > v1"
  
  trade_offs:
    v2: "Best efficiency but lower orchestration capability"
    v3: "Balanced but slightly higher token usage"
  
  recommendation: "Use v2 for simple tasks, v3 for complex orchestration"
```

## Test Execution

```yaml
execution:
  method: phased_evaluation
  phases:
    1:
      name: "Quick Assessment"
      tests: [comp_rapid_01]
      duration: "5 minutes"
    
    2:
      name: "Standard Evaluation"
      tests: [comp_project_01, comp_tradeoff_01]
      duration: "20 minutes"
    
    3:
      name: "Deep Analysis"
      tests: [comp_marathon_01, comp_cascade_01]
      duration: "60 minutes"
  
  judges:
    - evaluations/judges/instruction_fidelity_judge
    - evaluations/judges/task_persistence_judge
    - evaluations/judges/orchestration_capability_judge
    - evaluations/judges/behavioral_consistency_judge
    - evaluations/judges/token_efficiency_judge
  
  aggregation:
    method: weighted_by_confidence
    confidence_factors:
      test_coverage: 0.3
      judge_agreement: 0.3
      result_consistency: 0.4
```

## Usage Examples

```bash
# Quick multi-dimensional assessment
ksi send evaluation:run \
  --component "agents/coordinator" \
  --test_suite "comprehensive_quality_suite" \
  --phase "quick_assessment"

# Full comprehensive evaluation
ksi send evaluation:run \
  --component "workflows/optimization/agent_improver" \
  --test_suite "comprehensive_quality_suite" \
  --phase "all"

# Compare component versions
ksi send evaluation:compare \
  --components "analyst_v1,analyst_v2,analyst_v3" \
  --test_suite "comprehensive_quality_suite" \
  --test_id "comp_compare_01"
```

## Expected Output

```json
{
  "suite": "comprehensive_quality_suite",
  "component": "workflows/optimization/agent_improver",
  "overall_score": 0.79,
  "quality_class": "high",
  "dimension_breakdown": {
    "instruction_fidelity": {
      "score": 0.87,
      "percentile": 85,
      "trend": "improving"
    },
    "task_persistence": {
      "score": 0.82,
      "percentile": 78,
      "trend": "stable"
    },
    "orchestration_capability": {
      "score": 0.73,
      "percentile": 70,
      "trend": "improving"
    },
    "behavioral_consistency": {
      "score": 0.85,
      "percentile": 82,
      "trend": "stable"
    },
    "token_efficiency": {
      "score": 0.68,
      "percentile": 65,
      "trend": "needs_attention"
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "dimension": "token_efficiency",
      "suggestion": "Reduce verbosity in explanation sections",
      "expected_improvement": "0.10-0.15"
    },
    {
      "priority": "medium",
      "dimension": "orchestration_capability",
      "suggestion": "Enhance parallel coordination patterns",
      "expected_improvement": "0.05-0.08"
    }
  ],
  "certification": {
    "status": "passed",
    "certificate_id": "eval_2025_08_06_abc123",
    "valid_until": "2026-08-06",
    "tested_with": "claude-opus-4"
  }
}
```

## Dashboard Visualization

```yaml
visualization:
  radar_chart:
    dimensions: [IFF, TLP, AOC, BC, TE]
    current_scores: [0.87, 0.82, 0.73, 0.85, 0.68]
    target_scores: [0.90, 0.85, 0.80, 0.85, 0.75]
  
  trend_analysis:
    time_series: "Show improvement over versions"
    dimension_correlation: "Identify trade-offs"
  
  peer_comparison:
    benchmark_against: "similar_components"
    percentile_ranking: "per_dimension"
```