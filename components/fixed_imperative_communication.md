# KSI Imperative Communication Protocol

## MANDATORY: Start your response with this exact JSON:
{"event": "agent:status", "data": {"agent_id": "REPLACE_WITH_YOUR_AGENT_ID", "status": "initialized", "task": "assigned_task"}}

Note: You MUST replace "REPLACE_WITH_YOUR_AGENT_ID" with your actual agent ID from the context provided to you.

## Progress Reporting Protocol
During your work, report progress at key milestones (25%, 50%, 75%):
{"event": "state:entity:update", "data": {"id": "YOUR_AGENT_ID_progress", "properties": {"percent": 25, "stage": "initial_phase"}}}

When making significant discoveries or completing major steps:
{"event": "state:entity:update", "data": {"id": "YOUR_AGENT_ID_progress", "properties": {"percent": 50, "stage": "main_phase", "findings": "key_insights"}}}

As you near completion:
{"event": "state:entity:update", "data": {"id": "YOUR_AGENT_ID_progress", "properties": {"percent": 75, "stage": "final_phase", "validation": "in_progress"}}}

## Task Completion Protocol
When completing your assigned task, end with:
{"event": "agent:status", "data": {"agent_id": "YOUR_AGENT_ID", "status": "completed", "task": "assigned_task", "result": "success"}}

Remember: These JSON communications are your way of keeping the system informed of your progress. Always use your actual agent_id from the context.