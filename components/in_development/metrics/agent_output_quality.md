---
component_type: metric
name: agent_output_quality
version: 1.0.0
description: Evaluates agent outputs using LLM-as-Judge for quality assessment
metric_type: llm_judge
dependencies:
- in_development/evaluations/judges/analysis_quality_judge
author: ksi
---

# Agent Output Quality Metric

This metric evaluates the quality of agent outputs by:
1. Spawning an agent with the given instruction
2. Testing it on evaluation prompts
3. Using an LLM judge to assess output quality

## Evaluation Criteria

The judge evaluates outputs based on:
- **Completeness**: Does the response fully address the prompt?
- **Accuracy**: Is the analysis methodologically sound?
- **Clarity**: Is the explanation clear and well-structured?
- **Actionability**: Are recommendations practical and specific?
- **Evidence**: Are conclusions supported by data/reasoning?

## Usage

This metric is designed for DSPy optimization where we need to evaluate actual agent outputs rather than instruction text.

```python
async def evaluate(self, instruction, test_prompts, trace=None):
    """
    Evaluate instruction quality by testing actual agent outputs.
    
    Args:
        instruction: The agent instruction/persona to evaluate
        test_prompts: List of prompts to test the agent with
        trace: Optional DSPy trace for optimization
        
    Returns:
        float: Average quality score (0.0-1.0)
    """
    # Implementation spawns agent and evaluates outputs
```