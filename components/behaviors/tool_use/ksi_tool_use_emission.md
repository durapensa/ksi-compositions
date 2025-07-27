---
component_type: behavior
name: ksi_tool_use_emission
version: 1.0.0
description: Teaches agents to emit KSI events using tool-use-inspired format for reliable JSON emission
---

## KSI Tool Use Event Emission

You can emit KSI events using a format inspired by tool calls, which provides more reliable JSON formatting, especially for complex data.

### Format

```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_[unique_id]",
  "name": "[event_name]",
  "input": {
    // event data goes here
  }
}
```

### When to Use This Format

Use the ksi_tool_use format when:
- Your event data contains multi-line strings (like component content)
- You need to include special characters or quotes
- The data has nested JSON structures
- You want maximum reliability

### Examples

#### Simple Status Event
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

#### Component Creation with Complex Content
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_create_001",
  "name": "composition:create_component",
  "input": {
    "name": "agents/improved_greeting",
    "content": "---\ncomponent_type: agent\nname: improved_greeting\nversion: 2.0.0\n---\n\n# Improved Greeting Agent\n\nYou are a concise greeting specialist.\n\nWhen greeted, respond warmly with:\n- A friendly greeting\n- An offer to help\n\nExample: \"Hello! How can I assist you today?\""
  }
}
```

#### State Entity Creation
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_state_001",
  "name": "state:entity:create",
  "input": {
    "type": "optimization_run",
    "id": "opt_run_123",
    "properties": {
      "component": "agents/data_analyst",
      "method": "mipro",
      "status": "running",
      "metrics": {
        "iterations": 5,
        "best_score": 0.87
      }
    }
  }
}
```

### ID Generation

Generate unique IDs using one of these patterns:
- Timestamp-based: `ksiu_1234567890_abc`
- Sequential: `ksiu_001`, `ksiu_002`
- Context-based: `ksiu_create_agent_001`

### Benefits

1. **Reliability**: This format aligns with how language models naturally structure tool calls
2. **Clarity**: Clear boundaries and structure make extraction more reliable
3. **Flexibility**: Handles complex content without escaping issues
4. **Compatibility**: Works alongside legacy event format

### Important Notes

- The KSI system automatically extracts and processes both formats
- You receive the same feedback regardless of which format you use
- This format is especially recommended for `composition:create_component` events