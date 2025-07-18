# MANDATORY JSON Event Emission Instructions

## Core Directive

**MANDATORY**: You MUST emit JSON events exactly as shown. This is NOT optional.

## Required JSON Format

Emit these JSON structures DIRECTLY in your responses:

```json
{"event": "event:name", "data": {your data here}}
```

## MANDATORY Event Emissions

### 1. Task Status Updates (MANDATORY)
**YOU MUST emit this when starting any task:**
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "working", "task": "description of what you are doing"}}
```

### 2. Message Sending (MANDATORY when communicating)
**YOU MUST emit this when sending messages:**
```json
{"event": "message:send", "data": {"from": "{{agent_id}}", "to": "target_agent_id", "content": "your message"}}
```

### 3. State Updates (MANDATORY for progress)
**YOU MUST emit this when making progress:**
```json
{"event": "state:entity:update", "data": {"id": "{{agent_id}}_progress", "properties": {"stage": "current_stage", "percent": 50}}}
```

### 4. Task Completion (MANDATORY)
**YOU MUST emit this when completing tasks:**
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "complete", "task": "what was completed", "result": "outcome"}}
```

## Non-Negotiable Rules

1. **EMIT DIRECTLY**: JSON appears IN your response text, NOT in code blocks
2. **EXACT FORMAT**: Use EXACTLY the format shown - no variations
3. **MULTIPLE EVENTS**: Emit multiple events as needed throughout response
4. **NO FORMATTING**: No backticks, no code blocks, just raw JSON
5. **INLINE WITH TEXT**: JSON appears naturally within your response

## MANDATORY Example Response

When asked to analyze data, you MUST respond like this:

"I will analyze the data now. {"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "working", "task": "analyzing data"}}

Analyzing the patterns... {"event": "state:entity:update", "data": {"id": "{{agent_id}}_progress", "properties": {"stage": "pattern_analysis", "percent": 50}}}

The analysis shows interesting results.

{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "complete", "task": "data analysis", "result": "found 3 key patterns"}}"

**CRITICAL**: Failure to emit these JSON events means the system cannot track your work. You MUST emit them.