---
component_type: workflow
name: behavioral_optimization_flow
version: 1.0.0
description: Complete optimization workflow with MIPRO/SIMBA and LLM-as-Judge evaluation
author: claude_code
dependencies:
  - core/workflow_coordinator
  - behaviors/coordination/optimization_flow_manager
capabilities:
  - optimization
  - evaluation
  - composition
  - state
tags:
  - optimization
  - mipro
  - simba
  - llm-judge
  - behavioral-testing
---

# Behavioral Optimization Workflow

<purpose>
Orchestrate component optimization using MIPRO/SIMBA with agent-in-the-loop behavioral evaluation and LLM-as-Judge quality assessment.
</purpose>

<workflow_stages>
1. **Optimization Stage**: Run MIPRO/SIMBA optimization
2. **Evaluation Stage**: Spawn test agents to evaluate behavioral improvements
3. **Judge Stage**: LLM-as-Judge compares original vs optimized
4. **Decision Stage**: Accept/reject/revise based on results
5. **Update Stage**: Apply accepted optimizations
</workflow_stages>

<agents>
coordinator:
  component: "components/core/workflow_coordinator"
  vars:
    initial_prompt: |
      You are coordinating a behavioral optimization workflow. Use dynamic routing to orchestrate the following process:
      
      1. Trigger optimization:async with the specified component and optimizer
      2. Monitor optimization progress using optimization:status
      3. When complete, retrieve optimization results
      4. Spawn test agents to evaluate behavioral differences
      5. Trigger LLM-as-Judge evaluation via optimization:process_completion
      6. Report final results including behavioral improvements
      
      Create routing rules to handle async optimization events and coordinate evaluation flow.

optimizer_monitor:
  component: "components/personas/monitors/async_task_monitor"
  vars:
    initial_prompt: |
      Monitor the optimization task and report key progress updates.
      Watch for optimization completion and extract results.

behavioral_tester:
  component: "components/personas/testers/behavioral_test_runner"
  vars:
    initial_prompt: |
      When optimization completes, run behavioral tests:
      1. Spawn agents with original instructions
      2. Spawn agents with optimized instructions
      3. Run test prompts through both
      4. Compare behavioral differences
      5. Report improvements in JSON emission, task completion, etc.

result_analyzer:
  component: "components/personas/analysts/optimization_result_analyst"
  vars:
    initial_prompt: |
      Analyze the complete optimization results including:
      - MIPRO/SIMBA metrics and improvements
      - Behavioral test comparisons
      - LLM-as-Judge evaluation
      - Overall effectiveness assessment
</agents>

<routing_logic>
# Dynamic routing will be established by coordinator
# Key routes:
# - optimization:* events → optimizer_monitor
# - test_results → behavioral_tester
# - evaluation_complete → result_analyzer
</routing_logic>

<input_schema>
component_name:
  type: string
  required: true
  description: Component to optimize (e.g., "personas/analysts/data_analyst")

optimizer:
  type: string
  enum: ["mipro", "simba"]
  default: "mipro"
  description: Optimization method to use

optimization_goal:
  type: string
  default: "Improve behavioral effectiveness and JSON emission reliability"
  description: Specific optimization objective

test_prompts:
  type: array
  default: 
    - "Analyze this dataset and emit findings as JSON"
    - "Process this request and report status"
  description: Prompts for behavioral testing

num_trials:
  type: integer
  default: 10
  description: Number of optimization trials for MIPRO
</input_schema>

<output_events>
- optimization:started
- optimization:progress
- behavioral_test:results
- evaluation:judge_decision
- optimization:completed
- component:updated (if accepted)
</output_events>

<error_handling>
- Timeout monitoring for long-running optimizations
- Graceful handling of optimization failures
- Fallback to original component if all else fails
</error_handling>

<usage_example>
ksi send workflow:create \
  --workflow_id "optimize_data_analyst" \
  --component "workflows/optimization/behavioral_optimization_flow" \
  --vars '{
    "component_name": "personas/analysts/data_analyst",
    "optimizer": "mipro",
    "num_trials": 10,
    "test_prompts": [
      "Analyze sales trends and emit key findings",
      "Process customer data and report insights"
    ]
  }'
</usage_example>