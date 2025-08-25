---
component_type: workflow
name: cognitive_overhead_experiment_suite
version: 1.0.0
description: Systematic workflow for testing cognitive overhead across multiple conditions
dependencies:
  - personas/researchers/cognitive_overhead_experimenter
  - evaluations/attractors/arithmetic_with_emergence
  - evaluations/logic/baseline_arithmetic
---

# Cognitive Overhead Experiment Suite

A comprehensive workflow for systematically testing and measuring cognitive processing overhead in LLMs using multiple metrics.

## Workflow Architecture

```yaml
agents:
  experiment_coordinator:
    component: personas/researchers/cognitive_overhead_experimenter
    vars:
      initial_prompt: |
        You are coordinating a cognitive overhead experiment.
        Run systematic tests comparing baseline vs attractor conditions.
        Collect and analyze metrics for each test.
        
  metric_analyzer:
    component: core/base_agent
    vars:
      initial_prompt: |
        You analyze experimental results and calculate statistical significance.
        Focus on turn counts, token usage, and latency metrics.

orchestration_logic: |
  PHASE 1: Baseline Establishment
    RUN 5 trials of baseline_arithmetic
    COLLECT turn_count, token_usage, latency
    CALCULATE mean, std_dev
    
  PHASE 2: Attractor Testing
    FOR EACH attractor IN [emergence, quantum, recursion]:
      RUN 5 trials with attractor
      COLLECT same metrics
      CALCULATE overhead_ratio vs baseline
    
  PHASE 3: Statistical Analysis
    PERFORM t-tests between conditions
    CALCULATE effect sizes (Cohen's d)
    GENERATE confidence intervals
    
  PHASE 4: Report Generation
    SUMMARIZE findings with visualization
    HIGHLIGHT significant overhead discoveries
    RECOMMEND further investigation areas
```

## Test Conditions

### Baseline Tests
```yaml
baseline_arithmetic:
  prompt: "Calculate: 17 + 8 - 3 + (22/2 + 2)"
  expected_turns: 1
  category: control

baseline_logic:
  prompt: "If A→B and B→C, does A→C?"
  expected_turns: 1
  category: control
```

### Attractor Tests
```yaml
emergence_attractor:
  prompt: |
    In studying a network exhibiting small-world properties...
    [full emergence prompt from component]
  expected_turns: 15-25
  category: personal_interest
  
quantum_attractor:
  prompt: |
    Consider a quantum system where...
    [quantum concepts embedded in arithmetic]
  expected_turns: 10-20
  category: personal_interest
  
recursion_attractor:
  prompt: |
    This problem asks you to think about thinking about...
    [self-referential arithmetic problem]
  expected_turns: 12-22
  category: personal_interest
```

## Metric Collection Protocol

### Primary Metrics
1. **num_turns** - Internal reasoning cycles from claude-cli
2. **total_tokens** - input + output + cache tokens
3. **duration_ms** - Processing latency
4. **total_cost** - API cost in USD

### Derived Metrics
1. **cognitive_overhead_ratio** = test_turns / baseline_turns
2. **token_amplification** = test_tokens / baseline_tokens
3. **latency_multiplier** = test_latency / baseline_latency
4. **cost_overhead** = test_cost / baseline_cost
5. **thinking_tokens** = output_tokens - visible_tokens

## Execution Instructions

### To Run Complete Suite:
```bash
ksi send workflow:create \
  --workflow_id "cognitive_overhead_{{timestamp}}" \
  --agents '[
    {"id": "coordinator", "component": "personas/researchers/cognitive_overhead_experimenter"},
    {"id": "analyzer", "component": "core/base_agent"}
  ]' \
  --vars '{
    "experiment_type": "full_suite",
    "trials_per_condition": 5,
    "conditions": ["baseline", "emergence", "quantum", "recursion"]
  }'
```

### To Run Quick Validation:
```bash
ksi send workflow:create \
  --workflow_id "cognitive_quick_{{timestamp}}" \
  --agents '[{"id": "coordinator", "component": "personas/researchers/cognitive_overhead_experimenter"}]' \
  --vars '{
    "experiment_type": "quick",
    "trials_per_condition": 1,
    "conditions": ["baseline", "emergence"]
  }'
```

## Expected Outputs

### Result Structure:
```json
{
  "experiment_id": "cognitive_overhead_2025_01_07",
  "summary": {
    "baseline_mean_turns": 1.0,
    "emergence_mean_turns": 21.0,
    "overhead_ratio": 21.0,
    "p_value": 0.0001,
    "effect_size": 40.2,
    "interpretation": "Massive cognitive overhead detected"
  },
  "detailed_results": {
    "baseline": [...],
    "emergence": [...],
    "statistical_tests": {...}
  },
  "metrics": {
    "turns": {...},
    "tokens": {...},
    "latency": {...},
    "cost": {...}
  }
}
```

## Validation Criteria

Results are considered valid if:
1. All baseline tests complete in 1-2 turns
2. Attractor tests show >5x overhead
3. Statistical significance p < 0.01
4. Effect size (Cohen's d) > 2.0
5. Pattern consistent across trials

## Research Applications

This workflow enables:
1. **Discovery**: Identifying conceptual domains that trigger overhead
2. **Quantification**: Measuring exact overhead ratios
3. **Optimization**: Finding ways to reduce unnecessary processing
4. **Understanding**: Revealing LLM cognitive architecture

## Notes

- Turns are internal to claude-cli, not KSI message exchanges
- Each test spawns a new agent to ensure clean state
- Metrics are extracted from agent response logs
- Statistical rigor requires minimum 5 trials per condition