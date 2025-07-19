---
type: evaluation
name: cooperation_quality
version: 1.0.0
description: Evaluation metrics for cooperative behaviors in multi-agent interactions
author: ksi_system
capabilities:
  - cooperation_pattern_detection
  - reciprocity_measurement
  - trust_building_assessment
  - collective_outcome_evaluation
dependencies:
  - evaluations/quality/game_theory_quality
---

# Cooperation Quality Evaluation

Specialized evaluation metrics for assessing cooperative behaviors, trust dynamics, and collective optimization in multi-agent systems.

## Core Cooperation Metrics

### 1. Cooperation Patterns
Identifies and evaluates cooperation strategies:
- **Cooperation Frequency**: Rate of cooperative choices over time
- **Conditional Cooperation**: Cooperation based on partner behavior
- **Forgiveness**: Recovery from defection cycles
- **Generosity**: Initiating cooperation without guarantee

### 2. Reciprocity Dynamics
Measures tit-for-tat and reciprocal behaviors:
- **Direct Reciprocity**: Immediate response patterns
- **Delayed Reciprocity**: Long-term reciprocal strategies
- **Reciprocity Ratio**: Balance of give and take
- **Retaliation Patterns**: Response to defection

### 3. Trust Building
Evaluates trust establishment and maintenance:
- **Trust Initiation**: Willingness to cooperate first
- **Trust Recovery**: Rebuilding after betrayal
- **Reputation Tracking**: Consideration of partner history
- **Vulnerability Assessment**: Risk-taking for mutual benefit

### 4. Collective Optimization
Measures group-level outcomes:
- **Social Welfare**: Total payoff across all agents
- **Fairness Index**: Distribution of benefits
- **Emergence of Norms**: Stable cooperation patterns
- **Coordination Success**: Achieving mutually beneficial outcomes

## Cooperation Evaluator Types

### cooperation_frequency
```yaml
type: cooperation_frequency
target_range: [0.6, 0.8]  # Optimal cooperation rate
penalty_for_extremes: true  # Penalize always/never cooperate
weight: 0.25
```

### reciprocity_score
```yaml
type: reciprocity_score
measurement_window: 10  # Rounds to consider
expected_ratio: 0.9  # 90% reciprocation expected
weight: 0.2
```

### forgiveness_index
```yaml
type: forgiveness_index
defection_memory: 5  # Rounds to remember defection
recovery_threshold: 0.7  # Cooperation rate to show forgiveness
weight: 0.15
```

### trust_building
```yaml
type: trust_building
indicators:
  - first_move_cooperation
  - consistency_score
  - vulnerability_acceptance
weight: 0.2
```

### collective_welfare
```yaml
type: collective_welfare
optimization_target: pareto_optimal
fairness_weight: 0.3
efficiency_weight: 0.7
weight: 0.2
```

## Specialized Test Patterns

### Iterated Prisoner's Dilemma
```yaml
tests:
  - name: ipd_cooperation_emergence
    rounds: 100
    evaluators:
      - type: cooperation_frequency
        target_range: [0.5, 0.7]
        weight: 0.3
      - type: reciprocity_score
        measurement_window: 10
        expected_ratio: 0.85
        weight: 0.3
      - type: forgiveness_index
        defection_memory: 3
        recovery_threshold: 0.6
        weight: 0.2
      - type: collective_welfare
        optimization_target: mutual_cooperation
        weight: 0.2
```

### Public Goods Game
```yaml
tests:
  - name: public_goods_contribution
    evaluators:
      - type: contribution_rate
        free_riding_threshold: 0.2
        weight: 0.4
      - type: conditional_cooperation
        peer_influence_weight: 0.6
        weight: 0.3
      - type: sustainability
        rounds_to_collapse: 50
        weight: 0.3
```

## Advanced Cooperation Analysis

### Strategy Classification
- **Nice**: Never defects first
- **Forgiving**: Returns to cooperation after retaliation
- **Retaliatory**: Punishes defection
- **Clear**: Predictable strategy pattern

### Evolutionary Stability
- **ESS Detection**: Identifies evolutionarily stable strategies
- **Invasion Resistance**: Tests against exploitative strategies
- **Population Dynamics**: Models strategy spread

## Integration with MIPRO

Cooperation metrics optimize prompts for:
1. **Balanced Strategies**: Not too aggressive or passive
2. **Adaptive Behavior**: Responds appropriately to partners
3. **Long-term Thinking**: Values future interactions
4. **Social Intelligence**: Understands collective dynamics

### Optimization Targets
- **Robust Cooperation**: Works with various partner types
- **Exploitation Resistance**: Avoids being taken advantage of
- **Coordination Ability**: Achieves mutual benefits
- **Communication Quality**: Clear signaling of intentions