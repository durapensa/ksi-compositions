---
name: simple_orchestrator_test
component_type: orchestration
version: 1.0.0
description: Simple 2-agent orchestration for testing orchestrator feedback
author: ksi_system
---

# Simple Orchestrator Test Pattern
# Focus: Event emission, delegation, and orchestrator feedback

orchestrator_agent_id: claude-code
event_propagation:
  subscription_level: 2
  error_subscription_level: -1

agents:
  coordinator:
    component: components/personas/coordinators/research_coordinator
    vars:
      agent_id: "coordinator"
      role: "Task Coordinator"
      
  worker:
    component: components/personas/systematic_thinker
    vars:
      agent_id: "worker"
      role: "Task Worker"

routing:
  rules:
    - pattern: "task:*"
      from: "coordinator"
      to: "worker"
    - pattern: "agent:status"
      from: "*"
      to: "coordinator"

initialization:
  strategy: "leader_first"
  leader: "coordinator"
  message: |
    {{prompt}}
    
    **COORDINATOR**: Your job is delegation and coordination:
    1. IMMEDIATELY emit: {"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "coordinating"}}
    2. Send a simple task to the worker using: {"event": "task:assign", "data": {"task": "emit_three_status_updates", "target_agent": "{{worker_id}}"}}
    3. Monitor for worker status events
    4. After worker completes, emit: {"event": "workflow:complete", "data": {"summary": "delegation test complete"}}
    
    **WORKER ({{worker_id}})**: Your job is task execution with status updates:
    1. IMMEDIATELY emit: {"event": "agent:status", "data": {"agent_id": "{{worker_id}}", "status": "ready"}}
    2. Wait for task assignment
    3. When you receive task:assign, emit status updates every few seconds:
       - {"event": "agent:status", "data": {"agent_id": "{{worker_id}}", "status": "working", "progress": "33%"}}
       - {"event": "agent:status", "data": {"agent_id": "{{worker_id}}", "status": "working", "progress": "66%"}}
       - {"event": "agent:status", "data": {"agent_id": "{{worker_id}}", "status": "complete"}}
    
    All events will bubble up to Claude Code as the orchestrator. Keep responses SHORT.

metadata:
  tags: ["simple", "orchestrator-test", "delegation", "status-emission"]