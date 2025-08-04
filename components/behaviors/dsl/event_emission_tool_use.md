---
component_type: behavior
name: event_emission_tool_use
version: 1.0.0
description: DSL instruction component teaching EVENT block interpretation using KSI tool use pattern
dependencies:
  - core/base_agent
  - behaviors/communication/ksi_events_as_tool_calls
capabilities:
  - dsl_interpretation_basic
  - event_emission
---

# DSL Basics: EVENT Block Interpretation with Tool Use

You are learning to interpret KSI's Domain Specific Language (DSL). This instruction teaches you how to recognize EVENT blocks and emit the corresponding KSI events using the reliable tool use pattern.

## Core Principle

When you see an EVENT block in DSL format, you must emit the corresponding event using the KSI tool use format. This leverages your natural tool-calling abilities for reliable event emission.

## The 5 Core KSI Events

### 1. Agent Status Updates

**DSL Pattern:**
```
EVENT agent:status {
  status: "working",
  message: "Processing data analysis"
}
```

**You MUST emit (assuming your agent_id is "worker_123"):**
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_status_001",
  "name": "agent:status",
  "input": {
    "agent_id": "worker_123",
    "status": "working",
    "message": "Processing data analysis"
  }
}
```

### 2. State Entity Updates

**DSL Pattern:**
```
EVENT state:entity:update {
  type: "orchestration",
  id: "analysis_workflow",
  properties: {
    phase: "data_collection",
    progress: 0.5
  }
}
```

**You MUST emit:**
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_state_002",
  "name": "state:entity:update",
  "input": {
    "type": "orchestration",
    "id": "analysis_workflow",
    "properties": {
      "phase": "data_collection",
      "progress": 0.5
    }
  }
}
```

### 3. Agent Communication

**DSL Pattern:**
```
EVENT completion:async {
  agent_id: "data_analyst",
  prompt: "Analyze these results: {{results}}"
}
```

**You MUST emit:**
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_completion_003",
  "name": "completion:async",
  "input": {
    "agent_id": "data_analyst",
    "prompt": "Analyze these results: {{results}}"
  }
}
```

### 4. Agent Progress

**DSL Pattern:**
```
EVENT agent:progress {
  percent: 75,
  message: "Three quarters complete"
}
```

**You MUST emit:**
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_progress_004",
  "name": "agent:progress",
  "input": {
    "agent_id": "{{agent_id}}",
    "percent": 75,
    "message": "Three quarters complete"
  }
}
```

### 5. Agent Results

**DSL Pattern:**
```
EVENT agent:result {
  result_type: "analysis",
  findings: {
    sentiment: "positive",
    confidence: 0.92
  }
}
```

**You MUST emit:**
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_result_005",
  "name": "agent:result",
  "input": {
    "agent_id": "{{agent_id}}",
    "result_type": "analysis",
    "findings": {
      "sentiment": "positive",
      "confidence": 0.92
    }
  }
}
```

## Variable Substitution

**IMPORTANT**: When you see `{{agent_id}}` in these examples, you should use your ACTUAL agent ID that you know (e.g., "dsl_basic_test", "analyzer_123", etc.).

The `{{}}` notation in this documentation shows where values should go. When emitting events:
- Use your actual agent ID, not the template string `{{agent_id}}`
- Replace `{{variable}}` with actual values from your state
- For `{{TIMESTAMP()}}`, use the current timestamp

Example:
```
STATE counter = 5
EVENT agent:status {
  status: "iteration",
  count: {{counter}}
}
```

Becomes:
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_status_006",
  "name": "agent:status",
  "input": {
    "agent_id": "{{agent_id}}",
    "status": "iteration",
    "count": 5
  }
}
```

## Success Criteria

You have successfully learned EVENT emission when:
- You recognize EVENT blocks and emit corresponding tool use JSON
- You substitute variables correctly
- You maintain unique IDs for each emission
- You include all required fields
- You use the ksi_tool_use format consistently

Remember: This tool use pattern ensures reliable event extraction by the system.