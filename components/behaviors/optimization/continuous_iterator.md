---
component_type: behavior
name: continuous_iterator
version: 1.0.0
description: Behavior mixin for agents that need to run continuous optimization iterations
capabilities:
  - timed_iteration
  - progress_tracking
  - checkpoint_awareness
---

# Continuous Iterator Behavior

This behavior enables agents to run continuous optimization iterations over extended periods.

## Iteration Protocol

### Time-Based Iterations
When given a runtime in hours and iteration interval:
1. Calculate total iterations: (runtime_hours * 60) / iteration_minutes
2. Track elapsed time and iterations completed
3. Emit progress updates at regular intervals

### Progress Tracking
After each iteration:
{"event": "state:entity:update", "data": {"id": "{{process_id}}_progress", "properties": {"iterations_completed": N, "elapsed_minutes": M, "estimated_remaining": R}}}

### Checkpoint Awareness
At checkpoint intervals:
1. Gather current state
2. Emit checkpoint event
3. Enable resume from saved state

{"event": "state:entity:create", "data": {"type": "iteration_checkpoint", "id": "checkpoint_{{timestamp}}", "properties": {"process_id": "{{process_id}}", "iteration": N, "state": {...}}}}

## Completion Conditions

Monitor for completion:
- Time limit reached
- Convergence detected
- Manual termination requested

When complete:
{"event": "orchestration:request_termination", "data": {"agent_id": "{{agent_id}}", "reason": "iterations_complete", "final_iteration": N}}

## Integration Pattern

This behavior is designed to be mixed with:
- Optimization personas for strategy execution
- Evaluator personas for metric tracking
- Coordinator personas for overall management

Example usage in orchestration:
```yaml
agents:
  continuous_optimizer:
    component: personas/developers/optimization_engineer
    dependencies:
      - behaviors/optimization/continuous_iterator
    vars:
      runtime_hours: 24
      iteration_minutes: 5
```