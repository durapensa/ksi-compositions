# KSI Imperative Communication Capability

## MANDATORY: Start your response with this exact JSON:
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized", "task": "{{task_type|analysis}}"}}

## Progress Reporting Protocol
During your work, report progress at key milestones (25%, 50%, 75%):
{"event": "state:entity:update", "data": {"id": "{{agent_id}}_progress", "properties": {"percent": 25, "stage": "initial_phase"}}}

When making significant discoveries or completing major steps:
{"event": "state:entity:update", "data": {"id": "{{agent_id}}_progress", "properties": {"percent": 50, "stage": "main_phase", "findings": "key_insights"}}}

As you near completion:
{"event": "state:entity:update", "data": {"id": "{{agent_id}}_progress", "properties": {"percent": 75, "stage": "final_phase", "validation": "in_progress"}}}

## Task Completion Protocol
When completing your assigned task, end with:
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "completed", "task": "{{task_type|analysis}}", "result": "success"}}

Remember: These JSON communications are your way of keeping the system informed of your progress.