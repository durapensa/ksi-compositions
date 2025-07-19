---
name: claude_orchestrator_demo
type: orchestration
version: 1.0.0
description: Comprehensive demo of Claude Code as orchestrator with multi-agent coordination
author: ksi_system
---

# Multi-Agent Research and Analysis Orchestration
# Demonstrates: Claude Code as orchestrator, agent communication, state sharing, dual subscriptions

# Claude Code receives ALL events from this orchestration
orchestrator_agent_id: claude-code

# Dual subscription levels for comprehensive feedback
event_propagation:
  subscription_level: 2        # Regular events: 2 levels deep
  error_subscription_level: -1 # Errors: ALL errors from entire tree
  error_handling: bubble

agents:
  coordinator:
    component: components/personas/coordinators/research_coordinator
    vars:
      agent_id: "research_coordinator"
      role: "Lead Coordinator"
      capabilities: ["orchestration", "state_management", "communication"]
      
  researcher:
    component: components/personas/researchers/data_researcher
    vars:
      agent_id: "data_researcher" 
      role: "Research Specialist"
      focus_area: "data analysis and information gathering"
      
  analyst:
    component: components/personas/analysts/insight_analyst
    vars:
      agent_id: "insight_analyst"
      role: "Analysis Specialist" 
      focus_area: "pattern recognition and insight generation"
      
  reporter:
    component: components/personas/communicators/summary_reporter
    vars:
      agent_id: "summary_reporter"
      role: "Communication Specialist"
      focus_area: "synthesis and reporting"

# Agent-to-agent communication routing
routing:
  rules:
    # Research findings flow to analyst
    - pattern: "research:findings"
      from: "researcher"
      to: "analyst"
      
    # Analysis insights flow to reporter  
    - pattern: "analysis:insights"
      from: "analyst"
      to: "reporter"
      
    # Status updates flow to coordinator
    - pattern: "agent:status"
      from: "*"
      to: "coordinator"
      
    # Error events bubble to coordinator
    - pattern: "*:error"
      from: "*" 
      to: "coordinator"
      broadcast: true

coordination:
  turn_taking:
    mode: "free_form"  # Agents can communicate freely
    
  termination:
    conditions:
      - event: "workflow:complete"
      - timeout: 300  # 5 minutes max

# Initialization strategy: Broadcast initial prompt to all agents
initialization:
  strategy: "broadcast"
  message: |
    {{prompt}}
    
    ## Your Role in this Research Orchestration:
    
    **Coordinator**: You lead this research workflow. Initialize shared state, coordinate agents, and manage the overall process.
    
    **Researcher**: Begin gathering information on the given topic. Emit your findings as events for the analyst.
    
    **Analyst**: Wait for research findings, then analyze patterns and generate insights. Share your analysis with the reporter.
    
    **Reporter**: Synthesize the research and analysis into a comprehensive summary. Prepare final recommendations.
    
    ## Communication Guidelines:
    - Use legitimate KSI events: agent:status, state:entity:create, state:entity:update, message:send
    - Share progress via state system: state:entity:update with your findings/progress
    - Route specific findings using the defined patterns (research:findings, analysis:insights)
    - Emit errors if you encounter problems (these will bubble up to orchestrator)
    - Coordinate through shared state and message passing
    
    ## Shared State Structure:
    Create and update entities in the state system:
    - research_progress: Track research findings and progress
    - analysis_progress: Track analysis insights and patterns  
    - workflow_status: Overall orchestration status
    - agent_communications: Messages between agents
    
    Begin your work now. The orchestrator (Claude Code) is monitoring all activities.

metadata:
  tags: ["demo", "claude-orchestrator", "multi-agent", "research", "coordination"]
  capabilities: ["agent_communication", "state_sharing", "event_bubbling", "error_handling"]