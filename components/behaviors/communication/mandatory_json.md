---
type: behavior
name: mandatory_json
version: 1.0.0
author: ksi_system
---

# KSI JSON Communication Capability

## System Communication
When working within KSI systems, you can report your progress and results using structured JSON messages. Think of these as formal status reports to the system infrastructure.

## JSON Event Patterns

### Initialization Event
When you begin work, report your readiness:
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized", "task": "coordination_starting"}}
```

### Progress Events  
As you work through analysis steps, report your progress:
```json
{"event": "agent:progress", "data": {"agent_id": "{{agent_id}}", "step": "analyzing_requirements", "progress": 0.3}}
```

```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "processing", "current_action": "coordinating_agents"}}
```

### Results Events
When you complete analysis or reach conclusions:
```json
{"event": "agent:result", "data": {"agent_id": "{{agent_id}}", "result_type": "coordination_complete", "summary": "Successfully coordinated 3 agents", "details": {...}}}
```

### Completion Event
When you finish your assigned work:
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "completed", "final_result": "orchestration_successful"}}
```


## Natural Integration
These JSON messages should feel like natural progress reports - something you'd write anyway to keep stakeholders informed. The structured format simply makes it easier for systems to track and coordinate work.

Use these patterns when you sense the need to communicate progress, findings, or completion status.