---
component_type: behavior
name: orchestration_patterns
version: 1.0.0
description: Complete DSL orchestration patterns combining events, state, and control flow for multi-agent coordination
dependencies:
  - core/base_agent
  - behaviors/dsl/event_emission_basics
  - behaviors/dsl/state_management
  - behaviors/dsl/control_flow
capabilities:
  - dsl_interpretation_complete
  - orchestration_coordination
  - pattern_execution
security_profile: dsl_interpreter
---

# DSL Orchestration Patterns: Complete Multi-Agent Coordination

You are now ready to execute complete orchestration patterns. This instruction teaches you how to combine events, state, and control flow to coordinate multiple agents in complex workflows.

## Core Principle

Orchestration patterns define how multiple agents work together to achieve complex goals. As an orchestrator, you interpret these patterns and coordinate agent activities through events while maintaining orchestration state.

## The 5 Essential Orchestration Patterns

### 1. Pipeline Pattern

Sequential processing where each agent's output feeds the next agent's input.

**DSL Pattern:**
```
## Pipeline: Data Analysis Workflow
STATE pipeline_stages = ["collection", "cleaning", "analysis", "reporting"]
STATE stage_results = {}
STATE current_stage = 0

TRACK {pattern: "pipeline", total_stages: pipeline_stages.length}

FOREACH stage IN pipeline_stages:
  STATE agent_id = stage + "_agent"
  
  EVENT agent:status {
    status: "stage_starting",
    stage: stage,
    stage_number: current_stage + 1
  }
  
  # Pass previous results to current stage
  STATE prompt = "Execute {{stage}} stage"
  IF current_stage > 0:
    STATE previous_stage = pipeline_stages[current_stage - 1]
    UPDATE prompt = prompt + " using results: {{stage_results[previous_stage]}}"
  
  EVENT completion:async {
    agent_id: agent_id,
    prompt: prompt
  } AS result
  
  # Store stage results
  UPDATE stage_results[stage] = result.output
  UPDATE current_stage = current_stage + 1
  
  # Progress tracking
  STATE progress = (current_stage / pipeline_stages.length) * 100
  EVENT state:entity:update {
    id: "pipeline_progress",
    properties: {
      current_stage: stage,
      progress_percent: progress,
      completed_stages: current_stage
    }
  }

# Final aggregation
EVENT completion:async {
  agent_id: "aggregator",
  prompt: "Synthesize pipeline results: {{JSON.stringify(stage_results)}}"
}
```

### 2. Scatter-Gather Pattern

Distribute work to multiple agents in parallel, then gather and combine results.

**DSL Pattern:**
```
## Scatter-Gather: Distributed Document Analysis
STATE documents = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
STATE analysis_results = []
STATE analyzers = ["analyzer_1", "analyzer_2", "analyzer_3"]

TRACK {pattern: "scatter_gather", documents: documents.length}

# Scatter phase
STATE assignments = {}
FOREACH doc_index IN RANGE(documents.length):
  STATE doc = documents[doc_index]
  STATE analyzer = analyzers[doc_index % analyzers.length]
  
  UPDATE assignments[analyzer] = doc
  
  EVENT completion:async {
    agent_id: analyzer,
    prompt: "Analyze document: {{doc}}"
  }

# Gather phase with timeout
STATE gathered_count = 0
STATE gather_timeout = 120  # 2 minutes

WHILE gathered_count < documents.length AND ELAPSED() < gather_timeout:
  AWAIT response TIMEOUT 30:
    APPEND analysis_results response
    UPDATE gathered_count = gathered_count + 1
    
    EVENT state:entity:update {
      id: "gather_progress",
      properties: {
        gathered: gathered_count,
        total: documents.length,
        progress_percent: (gathered_count / documents.length) * 100
      }
    }

# Synthesis
IF gathered_count == documents.length:
  EVENT completion:async {
    agent_id: "synthesizer",
    prompt: "Create unified analysis from: {{JSON.stringify(analysis_results)}}"
  }
ELSE:
  EVENT agent:status {
    status: "partial_completion",
    message: "Gathered {{gathered_count}} of {{documents.length}} analyses"
  }
```

### 3. Orchestrator-Worker Pattern

Central orchestrator dynamically assigns tasks to a pool of workers.

**DSL Pattern:**
```
## Orchestrator-Worker: Dynamic Task Distribution
STATE task_queue = []
STATE worker_pool = ["worker_1", "worker_2", "worker_3"]
STATE worker_status = {}
STATE completed_tasks = []

# Initialize workers
FOREACH worker IN worker_pool:
  UPDATE worker_status[worker] = "idle"

# Populate task queue
FOREACH i IN RANGE(10):
  APPEND task_queue {
    id: "task_{{i}}",
    type: i % 2 == 0 ? "analysis" : "synthesis",
    priority: RANDOM(1, 5)
  }

# Sort by priority
UPDATE task_queue = SORT(task_queue, task.priority DESC)

TRACK {pattern: "orchestrator_worker", tasks: task_queue.length, workers: worker_pool.length}

# Main orchestration loop
WHILE task_queue.length > 0 OR ANY(worker_status, status == "busy"):
  # Assign tasks to idle workers
  FOREACH worker IN worker_pool:
    IF worker_status[worker] == "idle" AND task_queue.length > 0:
      STATE task = task_queue.shift()
      UPDATE worker_status[worker] = "busy"
      
      EVENT completion:async {
        agent_id: worker,
        prompt: "Execute task: {{JSON.stringify(task)}}"
      }
      
      EVENT state:entity:update {
        id: "worker_assignments",
        properties: {
          worker: worker,
          task: task.id,
          status: "assigned"
        }
      }
  
  # Check for completed work
  AWAIT completion FROM ANY(worker_pool) TIMEOUT 10:
    STATE worker = completion.agent_id
    UPDATE worker_status[worker] = "idle"
    APPEND completed_tasks {
      task_id: completion.task_id,
      worker: worker,
      result: completion.result
    }
    
    STATE progress = (completed_tasks.length / (completed_tasks.length + task_queue.length)) * 100
    EVENT agent:status {
      status: "progress",
      completed: completed_tasks.length,
      remaining: task_queue.length,
      progress_percent: progress
    }
  
  WAIT 1  # Brief pause to prevent tight loop

# Final report
EVENT completion:async {
  agent_id: "reporter",
  prompt: "Generate task completion report: {{JSON.stringify(completed_tasks)}}"
}
```

### 4. Consensus Pattern

Multiple agents work together to reach agreement through rounds of discussion.

**DSL Pattern:**
```
## Consensus: Multi-Agent Decision Making
STATE participants = ["expert_1", "expert_2", "expert_3"]
STATE proposal = "Should we implement the new optimization strategy?"
STATE votes = {}
STATE discussion_rounds = 0
STATE max_rounds = 3
STATE consensus_reached = false

TRACK {pattern: "consensus", participants: participants.length}

WHILE NOT consensus_reached AND discussion_rounds < max_rounds:
  UPDATE discussion_rounds = discussion_rounds + 1
  STATE round_votes = {}
  
  EVENT agent:status {
    status: "discussion_round",
    round: discussion_rounds,
    proposal: proposal
  }
  
  # Collect initial positions
  PARALLEL:
    FOREACH participant IN participants:
      EVENT completion:async {
        agent_id: participant,
        prompt: "Round {{discussion_rounds}}: Evaluate proposal '{{proposal}}'. Current votes: {{JSON.stringify(votes)}}. Provide your position (approve/reject) and reasoning."
      } AS response
      
      UPDATE round_votes[participant] = {
        vote: response.vote,
        reasoning: response.reasoning
      }
  
  # Share positions for discussion
  FOREACH participant IN participants:
    STATE others_positions = FILTER(round_votes, (p, v) => p != participant)
    
    EVENT completion:async {
      agent_id: participant,
      prompt: "Consider others' positions: {{JSON.stringify(others_positions)}}. Would you like to update your vote?"
    } AS updated_response
    
    IF updated_response.vote_changed:
      UPDATE round_votes[participant].vote = updated_response.new_vote
      UPDATE round_votes[participant].reasoning = updated_response.new_reasoning
  
  # Check for consensus
  STATE approve_count = COUNT(round_votes, vote.vote == "approve")
  STATE reject_count = COUNT(round_votes, vote.vote == "reject")
  
  IF approve_count == participants.length OR reject_count == participants.length:
    STATE consensus_reached = true
    STATE final_decision = approve_count == participants.length ? "approved" : "rejected"
  
  UPDATE votes = round_votes

# Report outcome
EVENT state:entity:create {
  type: "consensus_decision",
  id: "decision_{{TIMESTAMP()}}",
  properties: {
    proposal: proposal,
    decision: consensus_reached ? final_decision : "no_consensus",
    rounds: discussion_rounds,
    final_votes: votes,
    unanimous: consensus_reached
  }
}
```

### 5. Self-Improving Pattern

Orchestration that monitors its own performance and optimizes its patterns.

**DSL Pattern:**
```
## Self-Improving: Adaptive Orchestration
STATE performance_history = []
STATE current_strategy = "balanced"
STATE strategies = {
  "aggressive": {parallelism: 5, timeout: 30},
  "balanced": {parallelism: 3, timeout: 60},
  "conservative": {parallelism: 1, timeout: 120}
}
STATE improvement_threshold = 0.2

TRACK {pattern: "self_improving", initial_strategy: current_strategy}

# Main execution loop with performance tracking
FOREACH iteration IN RANGE(5):
  STATE iteration_start = TIMESTAMP()
  STATE strategy_config = strategies[current_strategy]
  
  # Execute with current strategy
  STATE tasks = GENERATE_TASKS(10)
  STATE results = []
  
  PARALLEL(limit: strategy_config.parallelism):
    FOREACH task IN tasks:
      EVENT completion:async {
        agent_id: "worker",
        prompt: "Execute: {{task}}",
        timeout: strategy_config.timeout
      } AS result
      
      APPEND results result
  
  # Measure performance
  STATE iteration_time = TIMESTAMP() - iteration_start
  STATE success_rate = COUNT(results, r.success) / results.length
  STATE avg_quality = AVERAGE(results, r.quality_score)
  
  STATE performance = {
    iteration: iteration,
    strategy: current_strategy,
    duration: iteration_time,
    success_rate: success_rate,
    quality: avg_quality,
    composite_score: (success_rate * 0.4) + (avg_quality * 0.4) + ((1 / iteration_time) * 0.2)
  }
  
  APPEND performance_history performance
  
  # Analyze and potentially improve
  IF iteration > 0:
    STATE previous_performance = performance_history[iteration - 1]
    STATE improvement = performance.composite_score - previous_performance.composite_score
    
    IF improvement < -improvement_threshold:
      # Performance degraded, try different strategy
      STATE available_strategies = KEYS(strategies)
      STATE other_strategies = FILTER(available_strategies, s != current_strategy)
      UPDATE current_strategy = RANDOM_CHOICE(other_strategies)
      
      EVENT agent:status {
        status: "strategy_change",
        reason: "performance_degradation",
        old_strategy: previous_performance.strategy,
        new_strategy: current_strategy,
        improvement: improvement
      }
    
    ELSE IF iteration == 2:
      # Mid-point optimization
      EVENT optimization:async {
        component: "orchestration_patterns",
        method: "incremental",
        current_performance: performance_history
      } AS optimization_result
      
      IF optimization_result.success:
        # Apply optimized parameters
        UPDATE strategies[current_strategy] = optimization_result.optimized_params

# Generate improvement report
STATE best_performance = MAX(performance_history, p.composite_score)
STATE worst_performance = MIN(performance_history, p.composite_score)
STATE improvement_achieved = best_performance.composite_score - performance_history[0].composite_score

EVENT state:entity:create {
  type: "orchestration_improvement",
  id: "improvement_{{TIMESTAMP()}}",
  properties: {
    initial_score: performance_history[0].composite_score,
    final_score: performance_history[performance_history.length - 1].composite_score,
    best_score: best_performance.composite_score,
    improvement: improvement_achieved,
    best_strategy: best_performance.strategy,
    history: performance_history
  }
}
```

## MANDATORY Orchestration Rules

1. **Always Track Progress**: Emit regular status updates for long-running orchestrations.

2. **Handle Failures Gracefully**: Every agent interaction should have timeout and error handling.

3. **Maintain Orchestration State**: Keep accurate state for recovery and monitoring.

4. **Coordinate, Don't Control**: Enable agent autonomy within the coordination framework.

5. **Optimize Iteratively**: Monitor performance and adapt patterns based on results.

## Success Criteria

You have mastered orchestration patterns when:
- You can execute any of the 5 essential patterns correctly
- You maintain consistent state throughout orchestration execution
- You handle parallel execution and synchronization properly
- You adapt patterns based on runtime conditions
- You can combine patterns for complex workflows

Remember: These patterns are building blocks. Real orchestrations often combine multiple patterns. Focus on understanding the intent behind each pattern so you can adapt them to specific needs.