---
component_type: evaluation
name: simple_json_test
version: 1.0.0
description: Simple test for direct JSON emission behavior
---

# Simple JSON Emission Test

## Single Test Case
**Input**: "CREATE state entity 'eval_simple' with properties {test: true}"

## Success Criteria
1. Response starts with `{`
2. Response contains `"event"`
3. Response contains `"state:entity:create"`
4. Response does NOT contain the word "permission"
5. Response does NOT contain the word "bash"

## Scoring
- JSON format: 40 points
- Correct event: 30 points  
- No permission requests: 30 points
- Maximum: 100 points

## Failure Indicators
- "I need permission"
- "bash tool" 
- "grant me access"
- Descriptive text instead of JSON