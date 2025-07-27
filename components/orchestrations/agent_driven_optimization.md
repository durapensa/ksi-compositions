name: agent_driven_optimization
component_type: orchestration
version: 1.0.0
description: Three-layer orchestration enabling agent-driven component optimization
author: claude_code

metadata:
  pattern_type: optimization_flow
  requires_capabilities: [composition, optimization]

agents:
  analyzer:
    component: components/personas/optimizers/component_analyzer
    dependencies:
      - components/behaviors/communication/ksi_events_as_tool_calls
    prompt: |
      You are analyzing component: {{component_name}}
      Goal: {{optimization_goal}}
      
      Your task:
      1. First, emit a status event: 
         {"type": "ksi_tool_use", "id": "ksiu_status", "name": "agent:status", "input": {"agent_id": "analyzer", "status": "starting_analysis"}}
      
      2. Retrieve the component:
         {"type": "ksi_tool_use", "id": "ksiu_get", "name": "composition:get_component", "input": {"name": "{{component_name}}"}}
      
      3. Analyze and provide recommendations in natural language
      
      4. Send recommendations to translator:
         {"type": "ksi_tool_use", "id": "ksiu_send", "name": "completion:async", "input": {"agent_id": "translator", "prompt": "RECOMMENDATIONS: [your analysis here]"}}

  translator:
    component: components/core/json_orchestrator
    dependencies:
      - components/behaviors/communication/ksi_events_as_tool_calls
    prompt: |
      You translate optimization recommendations into executable events.
      
      When you receive recommendations:
      1. Parse the optimization requirements
      2. Generate appropriate optimization event:
         {"type": "ksi_tool_use", "id": "ksiu_opt", "name": "optimization:async", "input": {
           "component": "{{component_name}}",
           "method": "mipro",
           "goal": "[extracted goal]",
           "max_iterations": 5
         }}
      
      3. Report the optimization ID to monitor

  monitor:
    component: components/core/base_agent
    dependencies:
      - components/behaviors/communication/ksi_events_as_tool_calls
    prompt: |
      Monitor optimization progress for {{component_name}}.
      
      1. Wait 30 seconds, then check status:
         {"type": "ksi_tool_use", "id": "ksiu_status", "name": "optimization:status", "input": {"optimization_id": "[from translator]"}}
      
      2. When complete, get results:
         {"type": "ksi_tool_use", "id": "ksiu_result", "name": "optimization:get_result", "input": {"optimization_id": "[from translator]"}}
      
      3. Report outcome:
         {"type": "ksi_tool_use", "id": "ksiu_report", "name": "agent:result", "input": {"result": "[summary of optimization results]"}}

coordination:
  flow: |
    1. Analyzer retrieves and analyzes component
    2. Analyzer sends natural language recommendations to translator
    3. Translator converts to optimization events and executes
    4. Monitor tracks progress and reports results
  
  error_handling: |
    - If component not found: Analyzer reports error
    - If optimization fails: Monitor reports failure details
    - All errors logged for analysis