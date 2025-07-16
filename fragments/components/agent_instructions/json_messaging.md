# JSON Event Emission Instructions

## Basic JSON Event Format

To communicate within the KSI system, emit JSON events directly in your responses:

```json
{"event": "event:name", "data": {your data here}}
```

## Core Messaging Events

### Send Message to Another Agent
```json
{"event": "agent:send_message", "data": {"agent_id": "target_agent_id", "message": {"content": "your message"}}}
```

### Track Your Actions
```json
{"event": "orchestration:track", "data": {"type": "action", "action": "what you did", "reason": "why you did it"}}
```

### Signal Completion
```json
{"event": "agent:task_complete", "data": {"task": "task description", "status": "success", "result": "task result"}}
```

## Important Rules

1. **EMIT DIRECTLY**: Include the actual JSON in your response text, not in code blocks
2. **VALID JSON**: Ensure proper JSON formatting with double quotes
3. **MULTIPLE EVENTS**: You can emit multiple events in a single response
4. **NO WRAPPING**: Don't wrap JSON in backticks or code blocks
5. **INLINE WITH TEXT**: JSON can appear anywhere in your response

Example response:
"I'll analyze the data now. {"event": "orchestration:track", "data": {"type": "action", "action": "starting_analysis"}} 
The analysis is complete. {"event": "agent:task_complete", "data": {"task": "data_analysis", "status": "success"}}"