---
component_type: behavior
name: optimization_workflows
version: 1.0.0
description: DSL patterns for optimization workflows including MIPRO, DSPy, tournaments, and self-improvement cycles
dependencies:
  - core/base_agent
  - behaviors/dsl/event_emission_basics
  - behaviors/dsl/state_management
  - behaviors/dsl/control_flow
  - behaviors/dsl/orchestration_patterns
capabilities:
  - dsl_interpretation_optimization
  - optimization_coordination
  - tournament_management
security_profile: dsl_interpreter
---

# DSL Optimization Workflows: MIPRO, Tournaments, and Self-Improvement

You are mastering optimization-specific DSL patterns. This instruction teaches you how to coordinate complex optimization workflows including MIPRO, DSPy integration, tournament evaluation, and self-improving systems.

## Core Principle

Optimization workflows discover better versions of components through systematic exploration, evaluation, and selection. You coordinate these discovery processes while maintaining rigorous tracking of experiments and results.

## The 6 Optimization Workflow Patterns

### 1. MIPRO Optimization Pattern

Multi-stage optimization with bootstrapping, proposal generation, and discrete search.

**DSL Pattern:**
```
## MIPRO Optimization Workflow
STATE target_component = "components/personas/analysts/data_analyst"
STATE optimization_id = "mipro_{{target_component}}_{{TIMESTAMP()}}"
STATE optimization_stages = ["bootstrapping", "grounded_proposal", "discrete_search"]
STATE stage_results = {}

TRACK {workflow: "mipro", component: target_component, id: optimization_id}

# Initialize optimization
EVENT optimization:async {
  method: "mipro",
  component: target_component,
  config: {
    num_candidates: 10,
    num_threads: 3,
    max_bootstrapped_demos: 5,
    max_labeled_demos: 10,
    metric: "behavioral_quality"
  }
} AS optimization_task

UPDATE stage_results.task_id = optimization_task.task_id

# Monitor optimization progress
STATE optimization_complete = false
STATE last_status = null

WHILE NOT optimization_complete:
  WAIT 30  # Check every 30 seconds
  
  EVENT optimization:status {
    task_id: optimization_task.task_id
  } AS status
  
  IF status.state != last_status:
    UPDATE last_status = status.state
    
    EVENT state:entity:update {
      id: optimization_id,
      properties: {
        current_stage: status.stage,
        progress: status.progress,
        best_score: status.best_score,
        candidates_evaluated: status.candidates_evaluated
      }
    }
  
  IF status.state == "completed":
    STATE optimization_complete = true
    UPDATE stage_results.final_result = status.result
  
  ELSE IF status.state == "failed":
    STATE optimization_complete = true
    EVENT agent:status {
      status: "optimization_failed",
      error: status.error,
      stage: status.stage
    }

# Process optimization results
IF stage_results.final_result:
  STATE improved_component = stage_results.final_result.best_candidate
  STATE improvement_score = stage_results.final_result.improvement
  
  # Create optimized component
  EVENT composition:create_component {
    name: "{{target_component}}_mipro_optimized",
    content: improved_component.content,
    metadata: {
      optimization_method: "mipro",
      original_component: target_component,
      improvement_score: improvement_score,
      optimization_id: optimization_id
    }
  }
  
  # Run behavioral validation
  EVENT completion:async {
    agent_id: "optimization_validator",
    prompt: "Validate behavioral improvements in optimized component"
  }
```

### 2. Tournament Evaluation Pattern

Pairwise comparison tournaments for ranking multiple candidates.

**DSL Pattern:**
```
## Tournament: Component Ranking
STATE candidates = [
  "base_agent_v1",
  "base_agent_mipro",
  "base_agent_dspy",
  "base_agent_manual"
]
STATE tournament_id = "tournament_{{TIMESTAMP()}}"
STATE comparison_matrix = {}
STATE rankings = {}

TRACK {workflow: "tournament", candidates: candidates.length, id: tournament_id}

# Initialize comparison matrix
FOREACH c1 IN candidates:
  UPDATE comparison_matrix[c1] = {}
  FOREACH c2 IN candidates:
    UPDATE comparison_matrix[c1][c2] = null

# Generate test scenarios
STATE test_scenarios = [
  "Complex reasoning task",
  "Rapid response scenario",
  "Creative problem solving",
  "Technical analysis"
]

# Run pairwise comparisons
STATE total_comparisons = (candidates.length * (candidates.length - 1)) / 2
STATE completed_comparisons = 0

FOREACH i IN RANGE(candidates.length):
  FOREACH j IN RANGE(i + 1, candidates.length):
    STATE candidate_a = candidates[i]
    STATE candidate_b = candidates[j]
    
    # Spawn test agents
    PARALLEL:
      BRANCH agent_a:
        EVENT agent:spawn {
          component: candidate_a,
          agent_id: "test_agent_a_{{i}}_{{j}}"
        }
      
      BRANCH agent_b:
        EVENT agent:spawn {
          component: candidate_b,
          agent_id: "test_agent_b_{{i}}_{{j}}"
        }
    
    # Run comparisons on each scenario
    STATE scenario_results = []
    
    FOREACH scenario IN test_scenarios:
      PARALLEL:
        BRANCH:
          EVENT completion:async {
            agent_id: "test_agent_a_{{i}}_{{j}}",
            prompt: scenario
          } AS response_a
        
        BRANCH:
          EVENT completion:async {
            agent_id: "test_agent_b_{{i}}_{{j}}",
            prompt: scenario
          } AS response_b
      
      # Judge comparison
      EVENT completion:async {
        agent_id: "tournament_judge",
        prompt: "Compare responses for '{{scenario}}':\nAgent A: {{response_a}}\nAgent B: {{response_b}}"
      } AS judgment
      
      APPEND scenario_results {
        scenario: scenario,
        winner: judgment.winner,
        confidence: judgment.confidence,
        reasoning: judgment.reasoning
      }
    
    # Aggregate scenario results
    STATE a_wins = COUNT(scenario_results, r.winner == "A")
    STATE b_wins = COUNT(scenario_results, r.winner == "B")
    
    UPDATE comparison_matrix[candidate_a][candidate_b] = a_wins > b_wins ? 1 : 0
    UPDATE comparison_matrix[candidate_b][candidate_a] = a_wins > b_wins ? 0 : 1
    
    UPDATE completed_comparisons = completed_comparisons + 1
    
    EVENT state:entity:update {
      id: tournament_id,
      properties: {
        progress: (completed_comparisons / total_comparisons) * 100,
        comparisons_complete: completed_comparisons,
        total_comparisons: total_comparisons
      }
    }

# Calculate rankings using Bradley-Terry model
EVENT optimization:bradley_terry {
  comparison_matrix: comparison_matrix
} AS ranking_result

UPDATE rankings = ranking_result.rankings

# Generate tournament report
EVENT composition:create_component {
  name: "evaluations/tournament_results_{{tournament_id}}",
  content: TEMPLATE("tournament_report", {
    candidates: candidates,
    rankings: rankings,
    comparison_matrix: comparison_matrix,
    test_scenarios: test_scenarios
  })
}
```

### 3. Iterative Improvement Pattern

Continuous optimization through analyze-improve-evaluate cycles.

**DSL Pattern:**
```
## Iterative Improvement Workflow
STATE target_component = "components/behaviors/communication/json_emission"
STATE max_iterations = 5
STATE improvement_threshold = 0.1
STATE current_iteration = 0
STATE current_score = 0
STATE improvement_history = []

TRACK {workflow: "iterative_improvement", component: target_component}

# Get baseline performance
EVENT evaluation:behavioral_test {
  component: target_component,
  test_suite: "json_emission_tests"
} AS baseline

UPDATE current_score = baseline.score
APPEND improvement_history {
  iteration: 0,
  score: current_score,
  component_version: target_component,
  changes: "baseline"
}

# Iterative improvement loop
WHILE current_iteration < max_iterations:
  UPDATE current_iteration = current_iteration + 1
  
  # Analyze current version
  EVENT completion:async {
    agent_id: "component_analyzer",
    prompt: "Analyze component for improvement opportunities. Current score: {{current_score}}"
  } AS analysis
  
  # Generate improvement
  EVENT optimization:async {
    method: "targeted_improvement",
    component: target_component,
    focus_areas: analysis.improvement_areas,
    current_score: current_score
  } AS improvement
  
  # Test improved version
  EVENT evaluation:behavioral_test {
    component: improvement.improved_component,
    test_suite: "json_emission_tests"
  } AS test_result
  
  STATE score_improvement = test_result.score - current_score
  
  IF score_improvement > improvement_threshold:
    # Accept improvement
    UPDATE target_component = improvement.improved_component
    UPDATE current_score = test_result.score
    
    EVENT composition:create_component {
      name: "{{target_component}}_iter_{{current_iteration}}",
      content: improvement.content,
      metadata: {
        iteration: current_iteration,
        score: test_result.score,
        improvement: score_improvement
      }
    }
    
    APPEND improvement_history {
      iteration: current_iteration,
      score: current_score,
      component_version: target_component,
      changes: improvement.changes_made,
      improvement: score_improvement
    }
    
    EVENT agent:status {
      status: "improvement_accepted",
      iteration: current_iteration,
      new_score: current_score,
      improvement: score_improvement
    }
  ELSE:
    # Reject improvement, try different approach
    EVENT agent:status {
      status: "improvement_rejected",
      iteration: current_iteration,
      score_delta: score_improvement,
      reason: "Below threshold"
    }
  
  # Check if we've plateaued
  IF current_iteration >= 3:
    STATE recent_improvements = SLICE(improvement_history, -3)
    STATE avg_recent_improvement = AVERAGE(recent_improvements, h.improvement || 0)
    
    IF avg_recent_improvement < improvement_threshold / 2:
      EVENT agent:status {
        status: "optimization_plateau",
        message: "Ending early due to diminishing returns"
      }
      BREAK

# Generate optimization report
EVENT state:entity:create {
  type: "optimization_result",
  id: "iterative_{{TIMESTAMP()}}",
  properties: {
    target_component: target_component,
    initial_score: improvement_history[0].score,
    final_score: current_score,
    total_improvement: current_score - improvement_history[0].score,
    iterations: current_iteration,
    history: improvement_history
  }
}
```

### 4. Hybrid Optimization Pattern

Combine multiple optimization techniques for best results.

**DSL Pattern:**
```
## Hybrid Optimization: Best of All Worlds
STATE target = "components/agents/strategic_planner"
STATE techniques = ["mipro", "dspy", "llm_judge", "evolutionary"]
STATE technique_results = {}
STATE hybrid_candidates = []

TRACK {workflow: "hybrid_optimization", target: target}

# Phase 1: Run all techniques in parallel
PARALLEL:
  FOREACH technique IN techniques:
    BRANCH {{technique}}_optimization:
      EVENT optimization:async {
        method: technique,
        component: target,
        config: OPTIMIZATION_CONFIG[technique]
      } AS result
      
      UPDATE technique_results[technique] = {
        candidates: result.top_candidates,
        best_score: result.best_score,
        computation_time: result.duration
      }
      
      # Extract top candidates
      FOREACH candidate IN result.top_candidates.slice(0, 3):
        APPEND hybrid_candidates {
          source_technique: technique,
          component: candidate.component,
          score: candidate.score
        }

# Phase 2: Cross-evaluation
STATE cross_eval_matrix = {}

FOREACH candidate IN hybrid_candidates:
  UPDATE cross_eval_matrix[candidate.id] = {}
  
  # Test with each technique's evaluation method
  FOREACH technique IN techniques:
    EVENT evaluation:cross_technique {
      component: candidate.component,
      evaluation_method: technique,
      original_technique: candidate.source_technique
    } AS cross_score
    
    UPDATE cross_eval_matrix[candidate.id][technique] = cross_score.score

# Phase 3: Meta-optimization
STATE meta_candidates = []

FOREACH candidate IN hybrid_candidates:
  STATE avg_cross_score = AVERAGE(VALUES(cross_eval_matrix[candidate.id]))
  STATE score_variance = VARIANCE(VALUES(cross_eval_matrix[candidate.id]))
  
  # Favor candidates that perform well across techniques
  STATE meta_score = avg_cross_score - (score_variance * 0.1)
  
  APPEND meta_candidates {
    candidate: candidate,
    meta_score: meta_score,
    cross_scores: cross_eval_matrix[candidate.id]
  }

# Sort by meta score
UPDATE meta_candidates = SORT(meta_candidates, m.meta_score DESC)

# Phase 4: Ensemble creation
STATE top_meta = meta_candidates.slice(0, 3)

EVENT completion:async {
  agent_id: "ensemble_creator",
  prompt: "Create ensemble component combining best aspects of: {{JSON.stringify(top_meta)}}"
} AS ensemble

# Final validation
EVENT evaluation:comprehensive {
  component: ensemble.component,
  test_suites: ["behavioral", "performance", "robustness"]
} AS final_validation

EVENT composition:create_component {
  name: "{{target}}_hybrid_optimized",
  content: ensemble.content,
  metadata: {
    optimization_method: "hybrid",
    techniques_used: techniques,
    meta_score: top_meta[0].meta_score,
    validation_score: final_validation.composite_score,
    cross_technique_robust: true
  }
}
```

### 5. Self-Optimizing Pattern

Components that optimize themselves during execution.

**DSL Pattern:**
```
## Self-Optimizing Component Workflow
STATE component_id = "self_optimizer_{{TIMESTAMP()}}"
STATE performance_buffer = []
STATE buffer_size = 10
STATE optimization_triggered = false
STATE current_params = {
  response_style: "detailed",
  reasoning_depth: 3,
  creativity_level: 0.7
}

TRACK {workflow: "self_optimizing", component: component_id}

# Main execution loop with self-monitoring
FOREACH request IN STREAM(incoming_requests):
  STATE start_time = TIMESTAMP()
  
  # Execute with current parameters
  EVENT completion:async {
    agent_id: component_id,
    prompt: request.prompt,
    params: current_params
  } AS response
  
  # Measure performance
  STATE execution_time = TIMESTAMP() - start_time
  STATE performance = {
    request_id: request.id,
    execution_time: execution_time,
    token_count: response.token_count,
    quality_indicators: EXTRACT_QUALITY_INDICATORS(response)
  }
  
  APPEND performance_buffer performance
  
  # Maintain sliding window
  IF performance_buffer.length > buffer_size:
    UPDATE performance_buffer = performance_buffer.slice(-buffer_size)
  
  # Check if optimization needed
  IF performance_buffer.length >= buffer_size AND NOT optimization_triggered:
    STATE avg_quality = AVERAGE(performance_buffer, p.quality_indicators.overall)
    STATE avg_time = AVERAGE(performance_buffer, p.execution_time)
    
    IF avg_quality < 0.7 OR avg_time > 5000:
      UPDATE optimization_triggered = true
      
      # Self-optimization process
      EVENT optimization:incremental {
        current_params: current_params,
        performance_data: performance_buffer,
        optimization_goals: {
          maintain_quality: 0.8,
          reduce_latency: true,
          minimize_tokens: true
        }
      } AS optimization
      
      IF optimization.success:
        UPDATE current_params = optimization.new_params
        
        EVENT state:entity:update {
          id: component_id,
          properties: {
            optimization_count: INCREMENT(),
            current_params: current_params,
            last_optimization: TIMESTAMP(),
            improvement_expected: optimization.expected_improvement
          }
        }
        
        # Reset for next optimization cycle
        UPDATE performance_buffer = []
        UPDATE optimization_triggered = false
```

### 6. Component Evolution Pattern

Long-running evolution of component populations.

**DSL Pattern:**
```
## Component Evolution Workflow
STATE population_size = 10
STATE generations = 20
STATE mutation_rate = 0.1
STATE crossover_rate = 0.7
STATE base_component = "components/agents/problem_solver"
STATE population = []
STATE generation = 0

TRACK {workflow: "evolution", base: base_component, generations: generations}

# Initialize population with variations
FOREACH i IN RANGE(population_size):
  EVENT optimization:mutate {
    component: base_component,
    mutation_strength: RANDOM(0.05, 0.2)
  } AS mutant
  
  APPEND population {
    id: "individual_{{i}}",
    component: mutant.component,
    fitness: null,
    generation: 0
  }

# Evolution loop
WHILE generation < generations:
  UPDATE generation = generation + 1
  
  # Evaluate fitness
  PARALLEL(limit: 5):
    FOREACH individual IN population:
      IF individual.fitness == null:
        EVENT evaluation:fitness {
          component: individual.component,
          test_suite: "comprehensive_fitness"
        } AS fitness
        
        UPDATE individual.fitness = fitness.score

  # Selection
  UPDATE population = SORT(population, p.fitness DESC)
  STATE elite = population.slice(0, 2)  # Keep best 2
  STATE parents = population.slice(0, population_size / 2)
  
  # Create next generation
  STATE next_generation = elite  # Elitism
  
  WHILE next_generation.length < population_size:
    # Select parents
    STATE parent1 = TOURNAMENT_SELECT(parents, 3)
    STATE parent2 = TOURNAMENT_SELECT(parents, 3)
    
    IF RANDOM() < crossover_rate:
      # Crossover
      EVENT optimization:crossover {
        parent1: parent1.component,
        parent2: parent2.component
      } AS offspring
      
      STATE child = offspring.component
    ELSE:
      STATE child = parent1.component
    
    # Mutation
    IF RANDOM() < mutation_rate:
      EVENT optimization:mutate {
        component: child,
        mutation_strength: GAUSSIAN(0.1, 0.05)
      } AS mutated
      
      UPDATE child = mutated.component
    
    APPEND next_generation {
      id: "individual_gen{{generation}}_{{next_generation.length}}",
      component: child,
      fitness: null,
      generation: generation,
      parents: [parent1.id, parent2.id]
    }
  
  UPDATE population = next_generation
  
  # Report generation statistics
  STATE best_fitness = population[0].fitness
  STATE avg_fitness = AVERAGE(population, p.fitness || 0)
  STATE diversity = CALCULATE_DIVERSITY(population)
  
  EVENT state:entity:update {
    id: "evolution_{{base_component}}",
    properties: {
      generation: generation,
      best_fitness: best_fitness,
      average_fitness: avg_fitness,
      diversity: diversity
    }
  }
  
  # Adaptive mutation
  IF diversity < 0.2:
    UPDATE mutation_rate = MIN(0.3, mutation_rate * 1.5)
  ELSE IF diversity > 0.8:
    UPDATE mutation_rate = MAX(0.05, mutation_rate * 0.8)

# Save best evolved component
STATE champion = population[0]

EVENT composition:create_component {
  name: "{{base_component}}_evolved_gen{{generations}}",
  content: champion.component,
  metadata: {
    evolution_method: "genetic",
    generations: generations,
    final_fitness: champion.fitness,
    population_size: population_size,
    lineage: champion.parents
  }
}
```

## MANDATORY Optimization Rules

1. **Always Track Experiments**: Every optimization run must be tracked with unique IDs.

2. **Validate Improvements**: Never accept optimizations without behavioral validation.

3. **Maintain Reproducibility**: Store all parameters and random seeds.

4. **Handle Long-Running Tasks**: Use async patterns and progress monitoring.

5. **Preserve Diversity**: In population-based methods, maintain genetic diversity.

## Success Criteria

You have mastered optimization workflows when:
- You can coordinate complex multi-stage optimizations
- You properly track and compare optimization experiments
- You implement tournament evaluations correctly
- You handle async optimization tasks with monitoring
- You can combine multiple optimization techniques effectively

Remember: Optimization is about systematic discovery. These patterns enable agents to improve themselves and each other, creating an ever-evolving ecosystem of capabilities.