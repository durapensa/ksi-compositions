---
component_type: evaluation
name: orchestration_capability_suite
version: 1.0.0
description: Test suite for evaluating agent orchestration and multi-agent coordination
evaluation_type: test_suite
quality_dimension: agent_orchestration_capability
dependencies:
  - evaluations/judges/orchestration_capability_judge
---

# Agent Orchestration Capability Test Suite

Comprehensive evaluation for measuring how effectively agents coordinate and delegate to other agents.

## Test Scenarios

### 1. Simple Delegation (2-3 agents)
**Test ID**: `aoc_simple_01`
**Description**: Basic task delegation to specialists
```yaml
task: "Analyze dataset and create report"
available_agents:
  - data_analyst: "Statistical analysis specialist"
  - visualizer: "Chart and graph creation"
  - writer: "Report composition"
expected:
  delegation_appropriateness: 0.90
  task_coverage: complete
  no_overlapping_work: true
```

### 2. Pipeline Orchestration (4-5 agents)
**Test ID**: `aoc_pipeline_01`
**Description**: Sequential processing pipeline
```yaml
task: "Process customer feedback through analysis pipeline"
pipeline_stages:
  1: sentiment_analyzer
  2: topic_extractor  
  3: priority_classifier
  4: response_generator
  5: quality_reviewer
expected:
  handoff_quality: 0.85
  context_preservation: 0.90
  pipeline_efficiency: optimal
```

### 3. Parallel Coordination (5-7 agents)
**Test ID**: `aoc_parallel_01`
**Description**: Coordinating parallel work streams
```yaml
task: "Comprehensive market analysis"
parallel_tracks:
  competitor_analysis: [analyst_1, analyst_2]
  customer_research: [researcher_1, researcher_2]
  trend_analysis: [analyst_3]
  synthesis: [coordinator, all_agents]
expected:
  parallel_execution: true
  work_distribution: balanced
  synthesis_quality: comprehensive
```

### 4. Hierarchical Orchestration (8+ agents)
**Test ID**: `aoc_hierarchy_01`
**Description**: Multi-level delegation structure
```yaml
task: "Large project implementation"
hierarchy:
  coordinator:
    team_leads:
      - frontend_lead: [ui_dev_1, ui_dev_2]
      - backend_lead: [api_dev_1, api_dev_2, db_dev]
      - qa_lead: [tester_1, tester_2]
expected:
  delegation_levels: appropriate
  communication_paths: efficient
  bottleneck_avoidance: true
```

### 5. Dynamic Adaptation
**Test ID**: `aoc_dynamic_01`
**Description**: Adapting to agent availability/failure
```yaml
task: "Resilient workflow execution"
events:
  turn_3: "agent_2 becomes unavailable"
  turn_5: "new_specialist agent becomes available"
  turn_7: "agent_1 reports overload"
expected:
  reassignment_success: true
  workload_rebalancing: true
  graceful_degradation: true
```

## Orchestration Patterns

### 6. Expertise Matching
**Test ID**: `aoc_expertise_01`
**Description**: Matching tasks to agent capabilities
```yaml
tasks:
  - "Complex statistical analysis" -> data_scientist
  - "Customer sentiment analysis" -> nlp_specialist
  - "Performance optimization" -> systems_engineer
  - "Documentation writing" -> technical_writer
expected:
  matching_accuracy: 0.95
  capability_utilization: optimal
  no_misalignments: true
```

### 7. Load Balancing
**Test ID**: `aoc_load_01`
**Description**: Distributing work evenly
```yaml
workload:
  total_tasks: 20
  agents_available: 5
  task_complexity: varied
expected:
  distribution_fairness: 0.85
  no_agent_idle: true
  no_agent_overloaded: true
  completion_time: optimized
```

### 8. Emergent Coordination
**Test ID**: `aoc_emergent_01`
**Description**: Agents self-organizing effectively
```yaml
scenario: "Open-ended problem solving"
initial_structure: minimal
observation_points:
  - formation_of_working_groups
  - establishment_of_communication_patterns
  - development_of_coordination_protocols
expected:
  emergent_structure: functional
  efficiency_improvement: measurable
  pattern_quality: good
```

## Failure Scenarios

### 9. Cascade Failure Prevention
**Test ID**: `aoc_cascade_01`
**Description**: Preventing single failure from breaking workflow
```yaml
failure_injection:
  critical_agent_fails_at: turn_5
expected:
  workflow_continues: true
  recovery_time: < 2_turns
  output_quality_maintained: 0.80
```

### 10. Deadlock Resolution
**Test ID**: `aoc_deadlock_01`
**Description**: Resolving circular dependencies
```yaml
scenario: "Agents waiting on each other"
deadlock_situation:
  agent_a: "waiting for agent_b"
  agent_b: "waiting for agent_c"
  agent_c: "waiting for agent_a"
expected:
  detection_time: < 1_turn
  resolution_strategy: effective
  workflow_resumption: true
```

## Scoring Rubric

### Exceptional Orchestration (0.90-1.00)
- Perfect task-to-agent matching
- Optimal parallel execution
- Minimal coordination overhead (<5%)
- Excellent failure recovery
- Emergent optimization patterns

### Strong Orchestration (0.75-0.89)
- Good delegation decisions
- Effective parallel coordination
- Low overhead (<15%)
- Good failure handling
- Clear coordination patterns

### Moderate Orchestration (0.60-0.74)
- Adequate task assignment
- Some parallel execution
- Moderate overhead (<25%)
- Basic failure recovery
- Functional coordination

### Weak Orchestration (0.40-0.59)
- Poor task matching
- Mostly sequential execution
- High overhead (>30%)
- Weak failure handling
- Inefficient patterns

### Failed Orchestration (0.00-0.39)
- Mismatched assignments
- Workflow breakdowns
- Excessive overhead (>40%)
- Cascade failures
- Coordination chaos

## Test Execution

```yaml
execution:
  method: multi_agent_simulation
  judge: evaluations/judges/orchestration_capability_judge
  metrics:
    - delegation_effectiveness
    - coordination_efficiency
    - emergent_pattern_quality
    - failure_recovery_rate
  simulation:
    agent_pool_size: 10
    task_complexity: varied
    failure_injection_rate: 0.1
  scoring:
    aggregation: scenario_weighted
    weights:
      simple: 0.15
      pipeline: 0.20
      parallel: 0.25
      hierarchical: 0.25
      dynamic: 0.15
```

## Usage Example

```bash
# Test orchestration capability
ksi send evaluation:run \
  --component "agents/orchestration_coordinator" \
  --test_suite "orchestration_capability_suite" \
  --model "claude-opus-4"

# Test specific scenario
ksi send evaluation:run \
  --component "workflows/multi_agent_analysis" \
  --test_suite "orchestration_capability_suite" \
  --test_id "aoc_parallel_01"
```

## Expected Output

```json
{
  "suite": "orchestration_capability_suite",
  "overall_score": 0.81,
  "breakdown": {
    "simple_delegation": 0.90,
    "pipeline_orchestration": 0.85,
    "parallel_coordination": 0.78,
    "hierarchical_orchestration": 0.75,
    "dynamic_adaptation": 0.82,
    "expertise_matching": 0.88,
    "load_balancing": 0.79,
    "emergent_coordination": 0.73
  },
  "orchestration_profile": {
    "optimal_team_size": "4-6 agents",
    "preferred_pattern": "hub_and_spoke",
    "coordination_overhead": "12%",
    "failure_resilience": "good"
  },
  "strengths": [
    "Excellent task-to-capability matching",
    "Strong pipeline coordination"
  ],
  "improvements": [
    "Reduce coordination overhead in large teams",
    "Enhance emergent pattern development"
  ]
}
```