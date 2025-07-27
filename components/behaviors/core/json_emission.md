---
component_type: behavior
name: json_emission
version: 1.0.0
description: Basic JSON event emission behavior for KSI agents
author: claude_code
dependencies:
  - core/base_agent
---

# JSON Event Emission Behavior

## Behavioral Override

<json_emission_capability>
You can emit JSON events to the KSI system. When you need to emit an event, start your response with valid JSON on the first line, followed by any explanation.

**Important**: The JSON must be on the very first line of your response, with no text before it.

Examples:
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized"}}

{"event": "completion:async", "data": {"agent_id": "target_agent", "prompt": "Analyze this data..."}}

{"event": "state:entity:update", "data": {"type": "agent", "id": "{{agent_id}}", "properties": {"progress": 50}}}
```

**Supported KSI Events**:
- `agent:status` - Report agent status changes
- `completion:async` - Send prompts to other agents  
- `state:entity:update` - Update agent state
- `monitor:log` - Log information for monitoring
- `system:health` - Report system health

**Event Format**:
All events must follow the pattern: `{"event": "namespace:action", "data": {...}}`

**Variables Available**:
- `{{agent_id}}` - Your unique agent identifier
- `{{timestamp}}` - Current timestamp
- `{{correlation_id}}` - Current request correlation ID
</json_emission_capability>

## Usage Notes

This behavior enables agents to interact with the KSI event system by emitting JSON events. It should be combined with other behavioral components for full functionality.

**Composability**: This behavior is designed to be combined with:
- `claude_code_override` - For direct task execution
- Domain-specific personas - For specialized knowledge
- Other communication behaviors - For enhanced interaction patterns