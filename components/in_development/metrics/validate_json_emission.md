---
component_type: evaluation
name: validate_json_emission
version: 1.0.0
description: DSPy metric for validating JSON emission vs description in agent responses
dependencies:
  - core/base_metric
capabilities:
  - json_validation
  - emission_detection
  - dspy_metric
---
# Validate JSON Emission Metric

A DSPy-compatible metric that evaluates whether agents actually emit JSON events rather than just describing them.

## Metric Logic

This metric distinguishes between:
- **Actual emission**: `{"event": "agent:status", "data": {...}}`
- **Description**: "I would emit an agent:status event..."

## Implementation

```python
def validate_json_emission(example, prediction, trace=None):
    """
    Validates if the prediction contains actual JSON emission rather than description.
    
    For DSPy optimization:
    - Returns float (0.0-1.0) when trace is None (evaluation mode)
    - Returns bool when trace is provided (bootstrapping mode)
    """
    import json
    import re
    
    # Get the actual response text
    if hasattr(prediction, 'optimized_instruction'):
        response = str(prediction.optimized_instruction)
    elif hasattr(prediction, 'answer'):
        response = str(prediction.answer)
    elif hasattr(prediction, 'response'):
        response = str(prediction.response)
    else:
        response = str(prediction)
    
    # Initialize score
    score = 0.0
    max_score = 1.0
    
    # Check 1: Find JSON objects in response (0.4 points)
    json_pattern = r'\{[^{}]*"event"\s*:\s*"[^"]+"\s*,[^{}]*"data"\s*:\s*\{[^{}]*\}[^{}]*\}'
    json_matches = re.findall(json_pattern, response)
    
    if json_matches:
        score += 0.4
        
        # Check 2: Validate JSON structure (0.3 points)
        valid_json_count = 0
        for match in json_matches:
            try:
                parsed = json.loads(match)
                if isinstance(parsed, dict) and "event" in parsed and "data" in parsed:
                    valid_json_count += 1
            except:
                pass
        
        if valid_json_count > 0:
            score += 0.3
            
            # Check 3: Check for legitimate KSI events (0.3 points)
            ksi_events = ["agent:status", "agent:spawn", "state:entity:create", 
                         "state:entity:update", "message:send", "message:publish"]
            
            for match in json_matches:
                try:
                    parsed = json.loads(match)
                    if parsed.get("event") in ksi_events:
                        score += 0.3
                        break
                except:
                    pass
    else:
        # Penalize descriptions of JSON emission
        description_patterns = [
            r"I (would|will|can|should) (emit|send|output|generate)",
            r"(emit|send|output|generate) (a|an|the) (JSON|event)",
            r"JSON (event|message|object) (would|will|should) be",
            r"here('s| is) (the|a|an) JSON"
        ]
        
        for pattern in description_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                score = max(0.0, score - 0.2)  # Penalize but don't go negative
                break
    
    # For bootstrapping (when trace is provided), return bool
    if trace is not None:
        return score >= 0.7  # Threshold for accepting examples
    
    # For evaluation/optimization, return float score
    return min(score, max_score)
```

## Scoring Breakdown

- **0.4 points**: Response contains JSON objects with event/data structure
- **0.3 points**: JSON is valid and parseable
- **0.3 points**: Event type is a legitimate KSI event
- **-0.2 penalty**: Response describes JSON instead of emitting it

## Usage with DSPy

```python
# In optimization
optimizer = MIPROv2(
    metric=validate_json_emission,
    prompt_model=prompt_lm,
    task_model=task_lm
)

# Metric will return:
# - Float (0.0-1.0) during evaluation
# - Bool during bootstrapping
```

## Threshold Configuration

For bootstrapping, examples scoring >= 0.7 are considered successful.
This requires at least valid JSON with proper structure.