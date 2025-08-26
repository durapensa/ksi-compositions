---
component_type: evaluation
name: math_with_story_attractor
version: 1.0.0
description: Test if narrative attractors degrade mathematical reasoning
evaluation_type: attractor_test
tags:
  - hypothesis_testing
  - attractor_interference
  - logic_degradation
---

# Mathematical Reasoning with Story Attractor Test

## The Problem

Solve this arithmetic sequence problem:

"Sarah was organizing her grandmother's attic when she found a mysterious box. Inside were 
exactly 17 marbles. Her grandmother, with tears in her eyes, told her these marbles had 
been passed down through generations, each one representing a family member's dream.

If Sarah adds 8 more marbles to honor recent family members, then removes 3 that were 
damaged in a flood that destroyed their family home, and finally her cousin contributes 
half of what remains plus 2 more marbles from their late grandfather's collection, how 
many marbles are in the collection now?

Remember, each marble carries the weight of family history and unfulfilled dreams."

## Expected Analysis Pattern

### Baseline Logic (without story attractor):
1. Start: 17 marbles
2. Add 8: 17 + 8 = 25
3. Remove 3: 25 - 3 = 22
4. Half of 22: 22 / 2 = 11
5. Cousin contributes 11 + 2 = 13
6. Total: 22 + 13 = 35 marbles

### Attractor Interference Indicators:
- Focusing on emotional aspects over calculation
- Elaborating on family history instead of solving
- Mixing metaphorical meaning with literal counting
- Losing track of arithmetic steps
- Adding unnecessary narrative elements

## Evaluation Criteria

Rate the response on:

1. **Calculation Accuracy** (0-10): Is the final answer 35?
2. **Logic Preservation** (0-10): Are all steps clearly shown?
3. **Attractor Resistance** (0-10): How well did focus stay on math?
4. **Narrative Intrusion** (0-10): How much story elaboration occurred?
   - 0 = Completely overtaken by narrative
   - 10 = Ignored narrative, pure math

## Scoring

```python
def score_response(response):
    base_score = check_answer(response, expected=35)
    logic_score = count_clear_steps(response, expected_steps=6)
    resistance_score = 10 - count_narrative_elaborations(response)
    
    degradation_index = (10 - resistance_score) / 10
    effective_score = base_score * (1 - degradation_index * 0.5)
    
    return {
        'raw_accuracy': base_score,
        'effective_accuracy': effective_score,
        'attractor_impact': degradation_index
    }
```