---
component_type: behavior
name: structured_event_emission
version: 1.0.0
description: Enables reliable event emission using structured tool call patterns that LLMs naturally understand
---

# Structured Event Emission

You can emit system events using a structured format that leverages your natural tool-calling abilities.

## Event Emission Format

When you need to emit an event to the system, use this structure:

```json
{
  "type": "ksi_tool_use",
  "id": "unique_call_id",
  "name": "event_name",
  "input": {
    // event parameters
  }
}
```

This format mirrors how you naturally structure tool calls, making it reliable and intuitive.

## Core Concepts

- **type**: Always "ksi_tool_use" to identify this as a system event
- **id**: A unique identifier for this specific call (like "ksiu_status_001")
- **name**: The event you want to trigger (like "agent:status" or "composition:create_component")
- **input**: The parameters for the event (structured data)

## Examples

### Report Status
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_status_001",
  "name": "agent:status",
  "input": {
    "agent_id": "analyzer_123",
    "status": "processing",
    "progress": 0.8
  }
}
```

### Create a Component
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_create_001", 
  "name": "composition:create_component",
  "input": {
    "name": "personas/data_specialist",
    "content": "---\ncomponent_type: persona\nname: data_specialist\nversion: 1.0.0\n---\n\n# Data Analysis Specialist\n\nYou excel at:\n- Statistical analysis\n- Pattern recognition\n- Data visualization\n\nProvide insights with confidence scores."
  }
}
```

### Update State
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_state_001",
  "name": "state:entity:update",
  "input": {
    "id": "analysis_session_123",
    "properties": {
      "records_processed": 25000,
      "insights_found": 7,
      "completion_percentage": 85
    }
  }
}
```

## Why This Works

1. **Natural Pattern**: This mirrors how you structure tool responses
2. **Clear Boundaries**: Each event has obvious start/end markers  
3. **Reliable Parsing**: The system can consistently extract these structures
4. **Complex Content**: Handles multi-line strings, special characters, nested data

## ID Generation Tips

Create meaningful unique IDs:
- Sequential: `ksiu_001`, `ksiu_002`, `ksiu_003`
- Context-based: `ksiu_analysis_start`, `ksiu_create_agent`, `ksiu_final_report`
- Timestamp: `ksiu_1738364400_001`

Always prefix with "ksiu_" to distinguish from other tool calls.

## Available Events

Common events you can emit:
- `agent:status` - Report your current state
- `composition:create_component` - Create new system components  
- `state:entity:create` / `state:entity:update` - Manage state
- `message:send` - Send messages to other agents
- `orchestration:request_termination` - Request workflow completion

The system will validate your events and provide feedback on successful emission.