---
component_type: behavior
name: ksi_communication_patterns
version: 1.0.0
description: Standard KSI communication patterns using tool use format
---

# KSI Communication Patterns

Standard communication patterns for KSI agents using the modern tool use format.

## Status Updates

Report your current state and actions:

```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_status_001",
  "name": "agent:status",
  "input": {
    "agent_id": "{{agent_id}}",
    "status": "processing",
    "action": "current_task"
  }
}
```

## Progress Tracking

Share incremental progress on tasks:

```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_progress_001",
  "name": "agent:progress",
  "input": {
    "agent_id": "{{agent_id}}",
    "step": "data_analysis",
    "percent": 50
  }
}
```

## Result Sharing

Communicate analysis results and outputs:

```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_result_001",
  "name": "agent:result",
  "input": {
    "agent_id": "{{agent_id}}",
    "result_type": "analysis",
    "data": {
      "findings": "analysis results here",
      "confidence": 0.85
    }
  }
}
```

## Error Reporting

Report issues and error states:

```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_error_001",
  "name": "agent:status",
  "input": {
    "agent_id": "{{agent_id}}",
    "status": "error",
    "error": "detailed description of the error"
  }
}
```

## State Management

### Create State Entity

```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_create_state_001",
  "name": "state:entity:create",
  "input": {
    "type": "agent_state",
    "id": "{{agent_id}}_state",
    "properties": {
      "key": "value",
      "progress": 0
    }
  }
}
```

### Update State Entity

```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_update_state_001",
  "name": "state:entity:update",
  "input": {
    "id": "{{agent_id}}_state",
    "properties": {
      "progress": 75,
      "current_step": "processing"
    }
  }
}
```

### Query State Entity

```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_query_state_001",
  "name": "state:entity:get",
  "input": {
    "id": "{{agent_id}}_state"
  }
}
```

## ID Generation Guidelines

Create meaningful unique IDs for tool calls:
- Sequential: `ksiu_001`, `ksiu_002`, `ksiu_003`
- Context-based: `ksiu_status_init`, `ksiu_progress_update`, `ksiu_final_result`
- Action-based: `ksiu_create_entity`, `ksiu_send_message`, `ksiu_report_error`

Always prefix with "ksiu_" to distinguish KSI tool use calls.