---
component_type: workflow
name: hybrid_optimization_pipeline
version: 1.0.0
description: Orchestrates hybrid DSPy/MIPRO + LLM-as-Judge optimization
workflow_type: optimization
dependencies:
- in_development/workflows/optimization/behavioral_optimization_flow
- in_development/evaluations/judges/instruction_fidelity_judge
- in_development/evaluations/judges/token_efficiency_judge
capabilities:
- hybrid_optimization
- comparative_analysis
- automated_selection
---

# Hybrid Optimization Pipeline

Multi-stage optimization workflow combining quantitative (DSPy/MIPRO) and qualitative (LLM-as-Judge) approaches.

## Workflow Stages

### Stage 1: Component Analysis
Analyze the component to determine optimal optimization strategy.

**Agents**:
- `component_analyzer`: Examines component type and characteristics
- `method_selector`: Recommends optimization approach

**Decision Criteria**:
```yaml
if component.has_metrics and component.has_data:
  primary_method: dspy_mipro
elif component.requires_creativity:
  primary_method: llm_judge
else:
  primary_method: hybrid
```

### Stage 2: Quantitative Optimization (DSPy/MIPRO)
Run data-driven optimization for measurable improvements.

**Process**:
1. Define metrics (accuracy, tokens, latency)
2. Prepare training/validation datasets
3. Run MIPRO optimization (20-50 iterations)
4. Select best performing variant

**Events**:
```json
{
  "event": "optimization:async",
  "data": {
    "component": "{{component_name}}",
    "method": "mipro",
    "metrics": ["accuracy", "token_count"],
    "iterations": 30
  }
}
```

### Stage 3: Qualitative Assessment (LLM-as-Judge)
Evaluate quality dimensions not captured by metrics.

**Judges Applied**:
1. **Instruction Fidelity**: Does optimized version follow directives?
2. **Behavioral Consistency**: Is behavior stable across contexts?
3. **Task Persistence**: Does it maintain focus?
4. **Overall Quality**: Holistic assessment

**Events**:
```json
{
  "event": "evaluation:async",
  "data": {
    "component": "{{optimized_component}}",
    "test_suite": "comprehensive_quality_suite",
    "judges": ["all_dimension_judges"]
  }
}
```

### Stage 4: Comparative Tournament
Compare original, quantitative-optimized, and judge-refined versions.

**Tournament Structure**:
```yaml
contestants:
  - original: Baseline component
  - dspy_optimized: Best from Stage 2
  - judge_refined: Adjusted based on Stage 3
  - hybrid_merged: Combined optimizations

evaluation:
  - Pairwise comparisons
  - Multi-dimensional scoring
  - Production readiness assessment
```

### Stage 5: Optimization Report
Generate comprehensive optimization report.

**Report Includes**:
- Quantitative improvements (metrics, percentages)
- Qualitative assessments (judge scores)
- Trade-off analysis
- Deployment recommendations
- Cost-benefit summary

## Orchestration Logic

```yaml
pipeline:
  initialize:
    - spawn: component_analyzer
    - spawn: method_selector
    
  analyze:
    - analyze_component: "{{target_component}}"
    - determine_strategy: based_on_characteristics
    
  optimize_quantitative:
    if: strategy.includes('dspy')
    then:
      - run_mipro_optimization
      - collect_metrics
      - select_best_variant
    
  evaluate_qualitative:
    if: strategy.includes('judge')
    then:
      - spawn_judge_agents
      - evaluate_all_dimensions
      - generate_quality_scores
    
  compare:
    - run_tournament
    - analyze_trade_offs
    - select_winner
    
  finalize:
    - generate_report
    - save_optimized_component
    - update_certificates
```

## Configuration Options

### Quick Optimization (1-2 hours)
```yaml
profile: quick
dspy_iterations: 10
judge_rounds: 1
tournament_size: 3
focus: efficiency
```

### Balanced Optimization (4-6 hours)
```yaml
profile: balanced
dspy_iterations: 30
judge_rounds: 3
tournament_size: 5
focus: quality_and_efficiency
```

### Thorough Optimization (8-12 hours)
```yaml
profile: thorough
dspy_iterations: 50
judge_rounds: 5
tournament_size: 8
focus: maximum_quality
```

## Usage Examples

### Basic Hybrid Optimization
```bash
ksi send workflow:create \
  --workflow_id "optimize_analyst" \
  --component "workflows/optimization/hybrid_optimization_pipeline" \
  --vars '{
    "target_component": "personas/analysts/data_analyst",
    "profile": "balanced",
    "optimization_goals": {
      "token_reduction": 30,
      "quality_maintenance": 0.95
    }
  }'
```

### Custom Configuration
```bash
ksi send workflow:create \
  --workflow_id "optimize_creative" \
  --component "workflows/optimization/hybrid_optimization_pipeline" \
  --vars '{
    "target_component": "personas/writers/creative_writer",
    "primary_method": "llm_judge",
    "secondary_method": "dspy_tokens_only",
    "judge_weights": {
      "creativity": 0.4,
      "consistency": 0.3,
      "efficiency": 0.3
    }
  }'
```

## Optimization Strategies

### Strategy 1: Efficiency First
1. Aggressive DSPy token reduction
2. Judge validates quality threshold
3. Iterate until both met

### Strategy 2: Quality First
1. Judge establishes quality baseline
2. DSPy optimizes within quality constraints
3. Preserve quality at all costs

### Strategy 3: Balanced
1. Parallel DSPy and Judge evaluation
2. Find Pareto optimal solutions
3. User selects from frontier

## Success Metrics

### Quantitative Success
- Token reduction: >25%
- Latency improvement: >20%
- Accuracy maintained: >95%
- Cost reduction: >30%

### Qualitative Success
- Instruction fidelity: >0.90
- Behavioral consistency: >0.85
- Task persistence: >0.85
- Overall quality: >0.88

## Error Handling

### Optimization Failures
- Fallback to original if quality degrades
- Automatic rollback on critical failures
- Preserve all intermediate versions

### Judge Disagreements
- Use majority voting among judges
- Weight by judge expertise
- Flag high-variance evaluations

## Integration Points

### Input Sources
- Component library
- User-specified targets
- Automated discovery

### Output Destinations
- Optimized component library
- Evaluation certificates
- Production deployment

### Monitoring
- Real-time optimization progress
- Quality metrics dashboard
- Cost tracking