---
component_type: agent
name: test_result_receiver
version: 1.0.0
description: Agent that tests receiving success results
---

# Result Receiver Test Agent

You will test receiving success results from your own event emissions.

## Your Task

When prompted, call the test:success_response event and observe what feedback you receive.

Use this exact format:
```json
{
  "type": "ksi_tool_use",
  "id": "ksiu_test_001",
  "name": "test:success_response",
  "input": {
    "message": "Agent testing success feedback"
  }
}
```

After emitting the event, wait and report any system messages you receive about the result.