# Test Agent ID Substitution

## MANDATORY: Start your response with this exact JSON:
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized", "task": "test"}}

You are agent {{agent_id}} testing variable substitution.

End with:
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "completed", "task": "test", "result": "success"}}