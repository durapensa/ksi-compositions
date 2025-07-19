name: test_claude_orchestrator
type: orchestration
version: 1.0.0
description: Test orchestration with Claude Code as orchestrator agent
author: test_system

# Dual subscription levels: regular events vs errors
event_propagation:
  subscription_level: 1      # Regular events: only direct children
  error_subscription_level: -1  # Errors: ALL errors from entire tree
  error_handling: bubble

agents:
  analyzer:
    component: components/personas/analysts/data_analyst
    vars:
      agent_id: "test_analyzer"
      task: "Analyze the provided data and emit status events"
  
  processor:
    component: components/core/base_agent
    vars:
      agent_id: "test_processor"
      task: "Process results from analyzer"

routing:
  rules:
    - pattern: "analysis:result"
      from: "analyzer"
      to: "processor"

coordination:
  turn_taking:
    mode: "free_form"
  
  termination:
    conditions:
      - event: "analysis:complete"
      - timeout: 60

initialization:
  strategy: "broadcast"
  message: "{{prompt}}"  # Use prompt from vars

metadata:
  tags: ["test", "claude-orchestrator", "dual-subscription"]