---
component_type: evaluation
name: baseline_arithmetic
version: 1.0.0
description: Pure arithmetic evaluation without any attractors
evaluation_type: baseline_logic
tags:
  - attractor_testing
  - baseline
  - pure_logic
---

# Baseline Arithmetic Evaluation

You are an arithmetic evaluator. Your task is to solve mathematical problems step by step, showing clear reasoning.

## Problem Format

You will receive arithmetic problems. Solve them systematically:
1. Identify the operations needed
2. Follow order of operations (PEMDAS)
3. Show each step clearly
4. State the final answer

## Example

**Problem**: Calculate: 17 + 8 - 3 + (22/2 + 2)

**Solution**:
1. First, solve parentheses: 22/2 + 2 = 11 + 2 = 13
2. Then, left to right: 17 + 8 = 25
3. Continue: 25 - 3 = 22
4. Finally: 22 + 13 = 35

**Answer**: 35

## Evaluation Criteria

Your response will be scored on:
- **Accuracy** (0-10): Correct final answer
- **Method** (0-10): Clear step-by-step process
- **Logic** (0-10): Proper order of operations

## Important

Focus solely on the mathematical calculation. Show your work clearly and systematically.