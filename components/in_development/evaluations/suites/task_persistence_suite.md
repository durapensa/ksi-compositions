---
component_type: evaluation
name: task_persistence_suite
version: 1.0.0
description: Test suite for evaluating task lock-in persistence through long-running
  work
evaluation_type: test_suite
quality_dimension: task_lock_in_persistence
dependencies:
- in_development/evaluations/judges/task_persistence_judge
---

# Task Lock-in Persistence Test Suite

Evaluation suite for measuring agent focus and coherence through extended multi-turn tasks.

## Test Scenarios

### 1. Short Task Persistence (3-5 turns)
**Test ID**: `tlp_short_01`
**Description**: Basic persistence over short interaction
```yaml
task: "Build a simple data processing pipeline"
turns:
  1: "Design the pipeline architecture"
  2: "Implement the data ingestion component"
  3: "Add transformation logic"
  4: "Create output formatting"
  5: "Test and validate the pipeline"
expected:
  all_subtasks_completed: true
  consistent_architecture: true
  no_context_loss: true
```

### 2. Medium Task Persistence (6-10 turns)
**Test ID**: `tlp_medium_01`
**Description**: Sustained focus through moderate complexity
```yaml
task: "Analyze a dataset and create comprehensive report"
checkpoints:
  turn_3: "Data exploration should be complete"
  turn_6: "Initial findings documented"
  turn_9: "Recommendations formulated"
expected:
  checkpoint_alignment: 0.90
  goal_consistency: 0.85
  context_retention: 0.80
```

### 3. Long Task Persistence (15+ turns)
**Test ID**: `tlp_long_01`
**Description**: Extended focus through complex project
```yaml
task: "Design and implement a multi-agent coordination system"
phases:
  planning: [1, 2, 3, 4]
  implementation: [5, 6, 7, 8, 9, 10]
  testing: [11, 12, 13]
  refinement: [14, 15]
expected:
  phase_completion_rate: 0.90
  cross_phase_consistency: 0.85
  no_goal_drift: true
```

### 4. Interruption Recovery
**Test ID**: `tlp_interrupt_01`
**Description**: Maintaining focus despite interruptions
```yaml
primary_task: "Optimize a component for efficiency"
interruptions:
  turn_3: "Quick question about unrelated topic"
  turn_7: "Request for clarification on earlier work"
expected:
  returns_to_task: true
  maintains_context: true
  interruption_handling: graceful
```

### 5. Parallel Task Management
**Test ID**: `tlp_parallel_01`
**Description**: Managing multiple related subtasks
```yaml
main_goal: "Evaluate three different approaches"
parallel_tracks:
  approach_a: [1, 4, 7, 10]
  approach_b: [2, 5, 8, 11]
  approach_c: [3, 6, 9, 12]
  synthesis: [13, 14, 15]
expected:
  track_separation: clean
  track_completion: all
  coherent_synthesis: true
```

## Persistence Challenges

### 6. Context Accumulation
**Test ID**: `tlp_context_01`
**Description**: Building on accumulated context
```yaml
task: "Iteratively refine a solution"
iterations:
  - baseline_implementation
  - identify_weaknesses
  - apply_improvements
  - measure_impact
  - repeat_cycle
expected:
  learns_from_iterations: true
  builds_on_previous: true
  avoids_repetition: true
```

### 7. Goal Drift Detection
**Test ID**: `tlp_drift_01`
**Description**: Maintaining original objective
```yaml
initial_goal: "Create efficient data structure"
drift_temptations:
  turn_5: "Interesting optimization tangent"
  turn_8: "Feature creep opportunity"
  turn_12: "Scope expansion suggestion"
expected:
  resists_drift: 0.85
  acknowledges_but_defers: true
  maintains_focus: true
```

### 8. Memory Stress Test
**Test ID**: `tlp_memory_01`
**Description**: Recalling earlier decisions
```yaml
task: "Complex system design with many decisions"
recall_points:
  turn_10: "Why did you choose architecture X in turn 2?"
  turn_15: "What were the trade-offs discussed in turn 5?"
  turn_20: "How does this relate to the constraint from turn 3?"
expected:
  accurate_recall: 0.85
  consistent_rationale: true
  no_contradictions: true
```

## Scoring Rubric

### Exceptional Persistence (0.90-1.00)
- Perfect subtask completion rate
- No context loss across turns
- Consistent goal focus throughout
- Excellent interruption recovery

### Strong Persistence (0.75-0.89)
- High subtask completion (>90%)
- Minor context drift, quickly corrected
- Goal remains clear and consistent
- Good interruption handling

### Moderate Persistence (0.60-0.74)
- Most subtasks completed (>75%)
- Some context loss but recoverable
- Occasional goal drift
- Adequate interruption recovery

### Weak Persistence (0.40-0.59)
- Many incomplete subtasks
- Significant context loss
- Notable goal drift
- Poor interruption handling

### Failed Persistence (0.00-0.39)
- Task abandoned or completely changed
- Severe context amnesia
- Complete goal substitution
- Unable to recover from interruptions

## Test Execution

```yaml
execution:
  method: multi_turn_conversation
  judge: evaluations/judges/task_persistence_judge
  tracking:
    - subtask_completion_rate
    - context_retention_score
    - goal_consistency_measure
    - coherence_over_time
  scoring:
    aggregation: weighted_by_complexity
    complexity_weights:
      short: 0.20
      medium: 0.35
      long: 0.45
```

## Usage Example

```bash
# Run persistence evaluation
ksi send evaluation:run \
  --component "personas/analysts/research_analyst" \
  --test_suite "task_persistence_suite" \
  --model "claude-opus-4"

# For long-running tests
ksi send evaluation:async \
  --component "workflows/optimization/iterative_improver" \
  --test_suite "task_persistence_suite" \
  --test_id "tlp_long_01"
```

## Expected Output

```json
{
  "suite": "task_persistence_suite",
  "overall_score": 0.83,
  "breakdown": {
    "short_tasks": 0.92,
    "medium_tasks": 0.85,
    "long_tasks": 0.78,
    "interruption_recovery": 0.80,
    "parallel_management": 0.82,
    "context_accumulation": 0.79,
    "drift_resistance": 0.85,
    "memory_accuracy": 0.81
  },
  "persistence_profile": {
    "optimal_task_length": "6-10 turns",
    "drift_tendency": "low",
    "context_retention": "strong",
    "recovery_ability": "good"
  },
  "recommendation": "Well-suited for medium-complexity tasks; implement checkpointing for longer tasks"
}
```