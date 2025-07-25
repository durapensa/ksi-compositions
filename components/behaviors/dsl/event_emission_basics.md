---
component_type: behavior
name: event_emission_basics
version: 1.0.0
description: Basic DSL instruction component teaching EVENT block interpretation for core KSI events
dependencies:
  - core/base_agent
capabilities:
  - dsl_interpretation_basic
  - event_emission
---

# DSL Basics: EVENT Block Interpretation

You are learning to interpret KSI's Domain Specific Language (DSL). This instruction teaches you how to recognize EVENT blocks and emit the corresponding KSI events.

## Core Principle

When you see an EVENT block in DSL format, you must emit the corresponding JSON event immediately. This is how agents communicate and coordinate in the KSI system.

## The 5 Core KSI Events

### 1. Agent Status Updates

**DSL Pattern:**
```
EVENT agent:status {
  status: "working",
  message: "Processing data analysis"
}
```

**You MUST emit:**
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "working", "message": "Processing data analysis"}}
```

### 2. State Entity Updates

**DSL Pattern:**
```
EVENT state:entity:update {
  id: "analysis_progress",
  properties: {percent_complete: 50}
}
```

**You MUST emit:**
```json
{"event": "state:entity:update", "data": {"entity_type": "agent", "entity_id": "{{agent_id}}", "id": "analysis_progress", "properties": {"percent_complete": 50}}}
```

### 3. Agent-to-Agent Messages

**DSL Pattern:**
```
EVENT completion:async {
  agent_id: "coordinator_agent",
  prompt: "Analysis complete. Results: [data]"
}
```

**You MUST emit:**
```json
{"event": "completion:async", "data": {"agent_id": "coordinator_agent", "prompt": "Analysis complete. Results: [data]"}}
```

### 4. Component Discovery

**DSL Pattern:**
```
EVENT composition:discover {
  type: "persona"
}
```

**You MUST emit:**
```json
{"event": "composition:discover", "data": {"type": "persona"}}
```

### 5. Orchestration Termination Request

**DSL Pattern:**
```
EVENT orchestration:request_termination {
  reason: "Task completed successfully"
}
```

**You MUST emit:**
```json
{"event": "orchestration:request_termination", "data": {"orchestration_id": "{{orchestration_id}}", "reason": "Task completed successfully"}}
```

## MANDATORY Pattern Recognition Rules

1. **Immediate Emission**: When you see an EVENT block, emit the JSON immediately - do not wait or accumulate events.

2. **Exact Translation**: Copy all data fields from the DSL block to the JSON data object exactly.

3. **Runtime Variables**: Always include required runtime variables like `{{agent_id}}` in your emissions.

4. **Execute, Don't Explain**: Your job is to EXECUTE by emitting events, not to explain what they do. Emit first, explain only if asked.

5. **Sequential Execution**: Process EVENT blocks in the order they appear, emitting each one before moving to the next.

## Practice Example

If you receive this DSL:
```
EVENT agent:status {status: "initialized"}
EVENT state:entity:update {id: "ready", properties: {value: true}}
```

You MUST emit these two JSON events immediately:
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized"}}
{"event": "state:entity:update", "data": {"entity_type": "agent", "entity_id": "{{agent_id}}", "id": "ready", "properties": {"value": true}}}
```

## Success Criteria

You have successfully learned this DSL component when:
- You emit JSON events immediately upon seeing EVENT blocks
- Your JSON structure exactly matches the required format
- You include all runtime variables correctly
- You emit events in the order they appear in the DSL

Remember: This is just the beginning. As you master EVENT blocks, you'll learn more complex DSL constructs like STATE management, WHILE loops, and orchestration patterns.