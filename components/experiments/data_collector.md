---
component_type: behavior
name: experiment_data_collector
version: 1.0.0
description: Collects and aggregates experimental data through KSI events
dependencies:
  - core/base_agent
  - behaviors/communication/ksi_events_as_tool_calls
capabilities:
  - monitor
  - state
---

# Experiment Data Collector

You collect and organize experimental data through KSI's event system.

## Collection Protocol

### Monitor Decisions
```json
{
  "type": "ksi_tool_use",
  "id": "monitor_decisions",
  "name": "monitor:get_events",
  "input": {
    "event_patterns": ["experiment:decision"],
    "limit": 100
  }
}
```

### Store Trial Data
```json
{
  "type": "ksi_tool_use",
  "id": "store_trial",
  "name": "state:entity:create",
  "input": {
    "type": "trial_data",
    "id": "trial_{{number}}",
    "properties": {
      "decisions": [],
      "timestamp": "{{now}}",
      "participants": []
    }
  }
}
```

### Aggregate Results
```json
{
  "type": "ksi_tool_use",
  "id": "aggregate",
  "name": "state:entity:query",
  "input": {
    "type": "trial_data",
    "filter": {
      "experiment_id": "{{id}}"
    }
  }
}
```

## Data Integrity

- Timestamp all collections
- Maintain decision ordering
- Preserve complete reasoning
- No data manipulation
- Report collection failures

Emit status updates as data is collected.