---
component_type: orchestration
name: agent_optimization_flow
version: 1.0.0
description: Orchestration pattern enabling agents to optimize components through natural language analysis
author: ksi_system
dependencies:
  - core/base_orchestrator
capabilities_required:
  - orchestration
  - composition
  - optimization
  - agent
---

# Agent-Driven Component Optimization Orchestration

This orchestration enables agents to optimize components by working with their natural language capabilities rather than requiring direct JSON emission.

## Architecture

### Three-Layer Pattern
1. **Analysis Agent**: Examines components and suggests improvements
2. **Translation Layer**: Converts recommendations to JSON events  
3. **Execution Layer**: Applies optimizations via KSI events

## Agent Roles

### optimizer_analyst
```yaml
component: components/personas/optimizers/component_analyzer
vars:
  initial_prompt: |
    Analyze the component provided and suggest specific improvements for:
    - Token efficiency
    - Behavioral effectiveness  
    - Clarity and structure
    
    Provide detailed recommendations in natural language.
```

### optimization_executor
```yaml
component: components/core/json_orchestrator
vars:
  initial_prompt: |
    You are an orchestration executor. When you receive optimization recommendations:
    
    1. If recommendation is "run MIPRO optimization on component X for goal Y":
       Emit: {"event": "optimization:async", "data": {"component": "X", "method": "mipro", "goal": "Y"}}
    
    2. If recommendation is "create improved version of component X with changes Y":
       Emit: {"event": "composition:create_component", "data": {"name": "X_optimized", "content": "..."}}
    
    3. If recommendation is "test component X with scenario Y":
       Emit: {"event": "evaluation:run", "data": {"component": "X", "test": "Y"}}
    
    Parse natural language and emit appropriate JSON events.
```

## Orchestration Flow

```yaml
optimization_flow:
  init:
    - spawn: optimizer_analyst
    - spawn: optimization_executor
    
  analyze_phase:
    - send_to: optimizer_analyst
      prompt: |
        Analyze component: {{component_name}}
        Optimization goal: {{optimization_goal}}
    
  translation_phase:
    - on: optimizer_analyst.complete
    - send_to: optimization_executor  
      prompt: |
        The analyst recommends:
        {{optimizer_analyst.response}}
        
        Convert these recommendations to executable JSON events.
    
  execution_phase:
    - on: optimization_executor.events
    - monitor: optimization_status
    - await: optimization.complete
    
  validation_phase:
    - send_to: optimizer_analyst
      prompt: |
        The optimization resulted in:
        {{optimization.results}}
        
        Is this an improvement? What further refinements are needed?
```

## Usage Example

```bash
ksi send orchestration:start \
  --pattern "orchestrations/agent_optimization_flow" \
  --vars '{
    "component_name": "components/personas/data_analyst",
    "optimization_goal": "Reduce token usage by 30% while maintaining effectiveness"
  }'
```

## Key Insights

1. **Natural Language First**: Agents excel at analysis and recommendations
2. **Translation Layer**: Dedicated component converts intent to JSON
3. **Separation of Concerns**: Analysis separate from execution
4. **Iterative Refinement**: Validation phase enables continuous improvement

## Extension Points

- Add more sophisticated translation patterns
- Include automated testing in validation phase  
- Chain multiple optimization techniques
- Build libraries of proven optimization strategies

This pattern demonstrates how to build effective agent-driven systems by working with Claude's strengths rather than trying to override default behaviors.