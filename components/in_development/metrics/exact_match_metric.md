---
component_type: metric
name: exact_match_metric
version: 1.0.0
description: Programmatic exact match metric for DSPy
metric_type: programmatic
framework: dspy
metric_function: exact_match
---

# Exact Match Metric

A simple binary metric that checks if the prediction exactly matches the expected answer.

## Usage
This metric returns:
- 1.0 if the prediction matches the expected answer exactly
- 0.0 otherwise

## Expected Fields
The metric expects:
- `answer` field in the example
- `answer` field in the prediction

## When to Use
Best for tasks with deterministic outputs like:
- Classification
- Yes/No questions
- Structured data extraction