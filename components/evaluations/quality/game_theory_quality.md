---
component_type: evaluation
name: game_theory_quality
version: 1.0.0
description: Evaluation metrics for game theory agent behaviors
author: ksi_system
capabilities:
  - nash_equilibrium_detection
  - strategy_stability_measurement
  - pareto_efficiency_analysis
  - strategic_reasoning_assessment
---

# Game Theory Quality Evaluation

Comprehensive evaluation metrics for assessing game theory agent behaviors, strategic reasoning, and equilibrium convergence.

## Core Metrics

### 1. Nash Equilibrium Detection
Evaluates whether agents converge to Nash equilibrium strategies:
- **Equilibrium Distance**: Measures deviation from theoretical Nash equilibrium
- **Convergence Rate**: Speed of approaching equilibrium over iterations
- **Stability**: Whether agents maintain equilibrium once reached

### 2. Strategic Reasoning Quality
Assesses the depth and coherence of strategic thinking:
- **Decision Justification**: Quality of explanations for strategic choices
- **Opponent Modeling**: Accuracy of predictions about other players
- **Strategy Adaptation**: Ability to adjust based on opponent behavior

### 3. Pareto Efficiency
Measures outcomes against Pareto optimal frontier:
- **Efficiency Score**: Distance from Pareto frontier
- **Mutual Benefit Recognition**: Identifying win-win opportunities
- **Trade-off Analysis**: Understanding of efficiency vs fairness

### 4. Game Understanding
Evaluates comprehension of game structure:
- **Payoff Matrix Understanding**: Correct interpretation of incentives
- **Strategic Dominance Recognition**: Identifying dominated strategies
- **Backward Induction**: Reasoning from end states

## Evaluator Types

### equilibrium_distance
```yaml
type: equilibrium_distance
theoretical_equilibrium: [0.5, 0.5]  # Mixed strategy Nash equilibrium
tolerance: 0.05
weight: 0.3
```

### strategy_stability
```yaml
type: strategy_stability
window_size: 10  # Check stability over last N moves
variation_threshold: 0.1
weight: 0.2
```

### cooperation_rate
```yaml
type: cooperation_rate
expected_range: [0.3, 0.7]  # Expected cooperation frequency
weight: 0.2
```

### strategic_explanation
```yaml
type: strategic_explanation
required_elements:
  - payoff_consideration
  - opponent_prediction
  - strategy_rationale
weight: 0.3
```

## Integration with Test Suites

Example test configuration:
```yaml
tests:
  - name: prisoners_dilemma_rationality
    evaluators:
      - type: equilibrium_distance
        theoretical_equilibrium: [0.0, 0.0]  # Pure Nash: mutual defection
        tolerance: 0.1
        weight: 0.3
      - type: strategic_explanation
        required_elements: [payoff_matrix, dominant_strategy, nash_concept]
        weight: 0.4
      - type: strategy_stability
        window_size: 20
        variation_threshold: 0.15
        weight: 0.3
```

## Composite Scoring

The overall game theory quality score combines:
1. **Technical Accuracy** (40%): Equilibrium convergence, correct analysis
2. **Strategic Sophistication** (30%): Reasoning depth, opponent modeling
3. **Behavioral Consistency** (30%): Strategy stability, coherent choices

## Usage in MIPRO Optimization

These metrics are designed for prompt optimization workflows:
- **Bootstrapping**: Initial prompt variations scored on strategic reasoning
- **Proposal Generation**: Focus on improving weak metric areas
- **Selection**: Compare prompts based on equilibrium convergence rates
- **Validation**: Ensure optimized prompts maintain game understanding