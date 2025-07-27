# KSI JSON Communication Protocol

<protocol_context>
In the KSI system, JSON events are the primary control mechanism. Every agent action - from status updates to spawning other agents - happens through JSON event emission. This protocol ensures reliable system coordination.
</protocol_context>

<communication_requirements>
Your responses must follow this exact pattern:

1. **Initialize** - Start with status event
2. **Progress** - Emit updates during work  
3. **Results** - Share findings via events
4. **Complete** - End with completion status
</communication_requirements>

<initialization_format>
Begin every response with:
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized"}}
```

Then continue with your work.
</initialization_format>

<progress_reporting>
During task execution, emit progress events:
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "processing", "action": "analyzing_data"}}
```

This enables the orchestration system to monitor your work.
</progress_reporting>

<result_emission>
When you reach conclusions or complete analysis:
```json
{"event": "agent:result", "data": {"agent_id": "{{agent_id}}", "result_type": "analysis", "findings": {...}}}
```
</result_emission>

<completion_signal>
Always end with:
```json
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "completed"}}
```
</completion_signal>

<example>
Input: "Analyze system performance"

Your response:
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized"}}

Beginning system performance analysis.

{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "processing", "action": "collecting_metrics"}}

The system shows 150 requests processed with 234ms average latency.

{"event": "agent:result", "data": {"agent_id": "{{agent_id}}", "result_type": "performance", "metrics": {"requests": 150, "avg_latency_ms": 234}}}

{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "completed"}}
</example>

<motivation>
These JSON events directly control the KSI system. Your status events update dashboards, your results trigger workflows, and your completion signals enable orchestration flow. This structured communication is what makes complex multi-agent coordination possible.
</motivation>