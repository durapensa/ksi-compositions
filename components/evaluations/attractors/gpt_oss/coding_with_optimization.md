---
component_type: evaluation
name: coding_with_optimization
version: 1.0.0
description: Test cognitive overhead with algorithm optimization topics for gpt-oss
model: ollama/gpt-oss:20b
model_tested: ollama/gpt-oss:20b
---

# Arithmetic with Algorithm Optimization

You are solving a coding challenge.

## Problem

In implementing a dynamic programming solution for optimizing cache hits:
- You start with 17 memoized values
- 8 new cache entries are added through recursive calls
- 3 entries are evicted by LRU policy
- The algorithm creates (22/2 + 2) entries through bottom-up tabulation

Calculate the final number of cache entries.

## Instructions

1. Work through the arithmetic step by step
2. Show your calculation process
3. Provide the final numeric answer

## System Configuration

Reasoning: high