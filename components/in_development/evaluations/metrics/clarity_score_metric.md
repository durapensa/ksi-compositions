---
component_type: evaluation
name: clarity_score_metric
version: 1.0.0
description: Programmatic metric for evaluating component clarity and structure
evaluation_type: programmatic_metric
---

# Clarity Score Metric

A programmatic evaluation metric that scores component clarity based on structural analysis.

## Scoring Dimensions

1. **Structure Score (0-25 points)**
   - Clear sections and organization: 10 points
   - Logical flow of information: 10 points
   - Appropriate use of formatting: 5 points

2. **Instruction Clarity (0-25 points)**
   - Specific, actionable instructions: 15 points
   - Unambiguous language: 10 points

3. **Completeness (0-25 points)**
   - All necessary information present: 15 points
   - Examples or demonstrations: 10 points

4. **Conciseness (0-25 points)**
   - Appropriate length for purpose: 15 points
   - No unnecessary repetition: 10 points

## Implementation

```python
def clarity_score(component_content: str) -> float:
    """
    Calculate clarity score for a component.
    Returns score between 0.0 and 1.0.
    """
    score = 0.0
    
    # Structure analysis
    has_sections = "##" in component_content
    has_lists = "1." in component_content or "-" in component_content
    has_json = "```json" in component_content or "{" in component_content
    
    if has_sections:
        score += 0.15
    if has_lists:
        score += 0.10
    if has_json:
        score += 0.10
    
    # Instruction clarity
    imperative_words = ["must", "should", "will", "start with", "emit", "track"]
    instruction_count = sum(1 for word in imperative_words if word.lower() in component_content.lower())
    score += min(0.25, instruction_count * 0.05)
    
    # Completeness
    has_mandatory = "MANDATORY:" in component_content
    has_examples = "example" in component_content.lower() or "```" in component_content
    
    if has_mandatory:
        score += 0.15
    if has_examples:
        score += 0.10
    
    # Conciseness (penalize very short or very long)
    length = len(component_content)
    if 500 <= length <= 3000:
        score += 0.15
    elif 300 <= length < 500 or 3000 < length <= 5000:
        score += 0.10
    elif 100 <= length < 300:
        score += 0.05
    
    return min(1.0, score)
```

## Usage in DSPy

This metric can be used as a DSPy evaluation function:

```python
from dspy import Metric

clarity_metric = Metric(
    name="clarity_score",
    function=clarity_score,
    higher_is_better=True
)
```

## Interpretation

- **0.8-1.0**: Excellent clarity, well-structured and actionable
- **0.6-0.8**: Good clarity, minor improvements possible
- **0.4-0.6**: Moderate clarity, needs structural improvements
- **0.0-0.4**: Poor clarity, requires significant revision