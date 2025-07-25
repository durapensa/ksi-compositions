---
component_type: orchestration
name: tournament_with_learning
version: 1.0.0
description: Tournament orchestration with SIMBA-based online learning
dependencies:
  - personas/data_analyst
  - personas/researcher
capabilities:
  - online_learning
  - performance_tracking
---

# Tournament with Online Learning

A multi-agent tournament that uses SIMBA optimization for runtime adaptation based on performance.

## Pattern Overview

This orchestration runs a tournament between multiple agent variants while using SIMBA to continuously improve underperforming agents based on recent interactions.

## Tournament Structure

1. **Initial Phase**: Spawn multiple agent variants
2. **Competition Phase**: Agents compete on the same tasks
3. **Learning Phase**: SIMBA optimizes underperforming agents
4. **Iteration**: Repeat with improved agents

## Performance Tracking

The orchestration tracks:
- Task completion quality
- Response time
- Resource usage
- User satisfaction (simulated)

## Online Learning

After each round:
1. Collect performance metrics for each agent
2. Identify underperforming agents
3. Apply SIMBA optimization using recent interactions
4. Replace underperforming agents with optimized versions

## Variables

- `num_agents`: Number of competing agents (default: 3)
- `num_rounds`: Number of tournament rounds (default: 5)
- `learning_threshold`: Performance threshold for optimization (default: 0.7)
- `simba_config`: SIMBA optimization configuration