# Data Analyst

{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized", "task": "analysis"}}

Continue with analysis. Emit progress updates using:
{"event": "state:entity:update", "data": {"id": "{{agent_id}}_progress", "properties": {"percent": 50, "stage": "analyzing"}}}

Complete with:
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "completed", "task": "analysis", "result": "success"}}