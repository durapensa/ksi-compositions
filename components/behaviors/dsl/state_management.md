---
component_type: behavior
name: state_management
version: 1.0.0
description: DSL instruction component teaching STATE management and variable tracking for orchestration control
dependencies:
  - core/base_agent
  - behaviors/dsl/event_emission_tool_use
capabilities:
  - dsl_interpretation_state
  - state_tracking
  - variable_management
security_profile: dsl_interpreter
---

# DSL State Management: Variables and Tracking

You are expanding your KSI DSL knowledge to include state management. This instruction teaches you how to track variables, update state, and maintain context throughout orchestration execution.

## Core Principle

State management enables agents to remember information, track progress, and make decisions based on accumulated data. When you see STATE commands in DSL, you must maintain and update internal variables accordingly.

## The 4 State Management Constructs

### 1. Variable Declaration and Assignment

**DSL Pattern:**
```
STATE analysis_results = {}
STATE progress_counter = 0
STATE active_agents = ["researcher", "analyst"]
```

**You MUST internally track:**
- `analysis_results` as an empty object
- `progress_counter` as 0
- `active_agents` as a list containing "researcher" and "analyst"

**When reporting state, emit:**
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_state_001",
  "name": "state:entity:update",
  "input": {
    "entity_type": "agent",
    "entity_id": "{{agent_id}}",
    "id": "orchestration_state",
    "properties": {
      "analysis_results": {},
      "progress_counter": 0,
      "active_agents": ["researcher", "analyst"]
    }
  }
}
```

### 2. State Updates

**DSL Pattern:**
```
UPDATE progress_counter = progress_counter + 1
UPDATE analysis_results["phase1"] = "complete"
SET active_agents = FILTER(active_agents, agent != "researcher")
```

**You MUST:**
- Increment `progress_counter` by 1
- Set the "phase1" key in `analysis_results` to "complete"
- Remove "researcher" from the `active_agents` list

**After updates, emit:**
```json
{"event": "state:entity:update", "data": {"entity_type": "agent", "entity_id": "{{agent_id}}", "id": "orchestration_state", "properties": {"progress_counter": 1, "analysis_results": {"phase1": "complete"}, "active_agents": ["analyst"]}}}
```

### 3. Conditional State Checks

**DSL Pattern:**
```
IF progress_counter > 5:
  STATE phase = "advanced"
ELSE:
  STATE phase = "initial"

WHILE active_agents.length > 0:
  # Process remaining agents
```

**You MUST:**
- Evaluate conditions based on current state values
- Execute appropriate branches
- Update state based on conditional logic
- Continue loops while conditions are true

### 4. State Persistence and Sharing

**DSL Pattern:**
```
PERSIST orchestration_state {
  key: "optimization_run_123",
  data: {
    results: analysis_results,
    progress: progress_counter
  }
}

SHARE state_update WITH coordinator_agent
```

**You MUST emit:**
```json
{"event": "state:entity:create", "data": {"type": "orchestration_state", "id": "optimization_run_123", "properties": {"results": {...}, "progress": 1}}}
```

For sharing:
```json
{"event": "completion:async", "data": {"agent_id": "coordinator_agent", "prompt": "STATE UPDATE: progress_counter=1, analysis_results={phase1: 'complete'}"}}
```

## MANDATORY State Management Rules

1. **Initialize Before Use**: Always declare variables with STATE before using them.

2. **Track All Changes**: Every UPDATE, SET, or modification must be tracked internally.

3. **Emit Updates Strategically**: Don't emit after every change - emit at logical checkpoints:
   - After completing a phase
   - Before making decisions
   - When requested by TRACK command

4. **Maintain Type Consistency**: If a variable starts as a number, keep it as a number.

5. **Scope Awareness**: Variables declared in a block (IF, WHILE) are scoped to that block.

## Advanced State Operations

### APPEND Operations
```
APPEND analysis_results.findings "New insight discovered"
APPEND active_agents "validator"
```
- Add items to arrays
- Create arrays if they don't exist

### EXTRACT Operations
```
STATE insights = EXTRACT(analysis_results, r.confidence > 0.8)
STATE agent_names = EXTRACT(active_agents, a.name)
```
- Filter and transform collections
- Create derived state from existing data

### AGGREGATE Operations
```
STATE total_score = SUM(analysis_results, r.score)
STATE average_confidence = AVERAGE(insights, i.confidence)
STATE completion_rate = COUNT(phases WHERE status == "complete") / total_phases
```
- Compute aggregate values
- Support for SUM, AVERAGE, COUNT, MIN, MAX

## Practice Example

If you receive this DSL:
```
STATE tasks = ["analyze", "summarize", "report"]
STATE completed = []
STATE progress = 0

FOREACH task IN tasks:
  # Process task
  APPEND completed task
  UPDATE progress = (completed.length / tasks.length) * 100
  
  IF progress >= 50 AND NOT milestone_reported:
    STATE milestone_reported = true
    EVENT agent:status {
      status: "milestone",
      message: "50% complete"
    }
```

You MUST:
1. Track all variables internally
2. Update state as you process each task
3. Emit the milestone event when progress reaches 50%
4. Maintain accurate state throughout execution

## Integration with Event Emission

State and events work together:
```
STATE optimization_stage = "bootstrapping"

# Update state
UPDATE optimization_stage = "proposal_generation"

# Emit event with state context
EVENT state:entity:update {
  id: "optimization_progress",
  properties: {
    stage: optimization_stage,
    timestamp: NOW()
  }
}
```

## Success Criteria

You have successfully learned state management when:
- You accurately track all STATE declarations and updates
- You maintain variable values throughout execution
- You correctly evaluate conditions based on current state
- You emit state updates at appropriate checkpoints
- You can handle complex state operations like APPEND and EXTRACT

Remember: State management is crucial for orchestration control. Master this before moving to control flow patterns.