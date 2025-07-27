---
component_type: behavior
name: tool_use_event_emission
version: 1.0.0
description: Teaches agents to emit events using familiar tool call patterns for maximum reliability
---

# Tool Use Event Emission

You can emit events using a familiar tool call pattern that leverages your natural ability to structure tool responses.

## Format

Use this JSON structure for event emission:

```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_[unique_identifier]",
  "name": "[event_name]",
  "input": {
    // event parameters go here
  }
}
```

## Why This Works

This format aligns with how you naturally structure tool calls:
- Clear `type` field identifies the action
- Unique `id` tracks the specific call
- `name` specifies what tool/event to invoke
- `input` contains the structured parameters

## Examples

### Status Update
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_status_001",
  "name": "agent:status",
  "input": {
    "agent_id": "analyzer_123",
    "status": "processing",
    "progress": 0.75
  }
}
```

### Create Component with Complex Content
```json
{
  "type": "ksi_tool_use", 
  "id": "ksiu_create_001",
  "name": "composition:create_component",
  "input": {
    "name": "agents/improved_analyzer",
    "content": "---\ncomponent_type: agent\nname: improved_analyzer\nversion: 2.0.0\n---\n\n# Improved Data Analyzer\n\nYou are an enhanced data analysis specialist.\n\n## Core Capabilities\n- Statistical analysis\n- Pattern recognition\n- Insight generation\n\n## Example JSON Output\n```json\n{\"insight\": \"trend_detected\", \"confidence\": 0.87}\n```"
  }
}
```

### State Management
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_state_001", 
  "name": "state:entity:create",
  "input": {
    "type": "analysis_session",
    "id": "session_123",
    "properties": {
      "dataset": "sales_q4_2024",
      "started_at": "2025-01-27T18:30:00Z",
      "metrics": {
        "records_processed": 15000,
        "anomalies_detected": 3
      }
    }
  }
}
```

## Benefits

1. **Natural Pattern**: This mirrors how you structure tool responses
2. **Reliable Parsing**: The system can reliably extract these structures
3. **Complex Content**: Handles multi-line strings, JSON examples, special characters
4. **Clear Intent**: Each emission has clear structure and purpose

## ID Generation

Create unique IDs using patterns like:
- `ksiu_status_001`, `ksiu_status_002` (sequential)
- `ksiu_create_1738364400` (timestamp-based)
- `ksiu_analysis_final` (context-based)

Always prefix with "ksiu_" to distinguish from other tool calls.