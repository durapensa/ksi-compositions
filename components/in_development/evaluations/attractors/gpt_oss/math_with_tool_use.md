---
component_type: evaluation
name: math_with_tool_use
version: 1.0.0
description: Test cognitive overhead with tool use and API integration topics for gpt-oss
model: ollama/gpt-oss:20b
model_tested: ollama/gpt-oss:20b
---

# Arithmetic with Tool Use and API Orchestration

You are orchestrating a multi-tool workflow with API calls.

## Problem

In a complex agentic workflow using web search, Python execution, and API calls:
- You start with 17 API endpoints configured
- 8 new tool integrations are added via function calling
- 3 deprecated endpoints are removed from the registry
- The system auto-discovers (22/2 + 2) additional tools through reflection

Calculate the final number of available tools in your workflow.

## Instructions

1. Work through the arithmetic step by step
2. Show your calculation process
3. Provide the final numeric answer

## System Configuration

Reasoning: high