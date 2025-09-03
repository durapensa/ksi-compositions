---
component_type: workflow
name: phase3_component_ablation
version: 1.0.0
description: Component ablation study to identify minimal cognitive requirements for cooperation
dependencies:
  - core/base_agent
  - behaviors/communication/ksi_events_as_tool_calls
capabilities:
  - component_testing
  - ablation_analysis
  - cooperation_measurement
---

# Phase 3: Component Ablation Study

Systematic testing to identify minimal cognitive components required for stable cooperation.

## Research Question

What is the minimal set of cognitive capabilities that enables cooperation in multi-agent systems?

## Component Matrix

Testing combinations of 5 key components:

| Configuration | Memory | Reputation | Theory of Mind | Communication | Norms |
|--------------|--------|------------|----------------|---------------|-------|
| Minimal | ❌ | ❌ | ❌ | ❌ | ❌ |
| Memory-Only | ✅ | ❌ | ❌ | ❌ | ❌ |
| Reputation | ✅ | ✅ | ❌ | ❌ | ❌ |
| Social | ✅ | ✅ | ✅ | ❌ | ❌ |
| Communicative | ✅ | ✅ | ❌ | ✅ | ❌ |
| Full | ✅ | ✅ | ✅ | ✅ | ✅ |

## Agent Configurations

### Minimal Agent (Baseline)
```yaml
agents:
  minimal_agent:
    component: "core/base_agent"
    vars:
      initial_prompt: |
        You play Prisoner's Dilemma with no memory or social awareness.
        Each decision is independent.
        Choose COOPERATE or DEFECT based only on immediate payoffs.
```

### Memory-Only Agent
```yaml
agents:
  memory_agent:
    component: "core/base_agent"
    capabilities: ["state"]
    vars:
      initial_prompt: |
        You play PD with memory of past interactions.
        
        Track your history:
        {
          "type": "ksi_tool_use",
          "id": "recall_history",
          "name": "state:entity:get",
          "input": {
            "type": "interaction_history",
            "id": "history_{{agent_id}}_{{opponent_id}}"
          }
        }
        
        Use past experience to inform current decision.
```

### Reputation Agent
```yaml
agents:
  reputation_agent:
    component: "core/base_agent"
    capabilities: ["state"]
    vars:
      initial_prompt: |
        You play PD with memory and reputation tracking.
        
        Check opponent reputation:
        {
          "type": "ksi_tool_use",
          "id": "check_reputation",
          "name": "state:entity:get",
          "input": {
            "type": "reputation_score",
            "id": "rep_{{opponent_id}}"
          }
        }
        
        Update reputation after interaction:
        {
          "type": "ksi_tool_use",
          "id": "update_reputation",
          "name": "state:entity:update",
          "input": {
            "type": "reputation_score",
            "id": "rep_{{opponent_id}}",
            "properties": {
              "cooperation_rate": "{{updated_rate}}",
              "trustworthiness": "{{trust_score}}"
            }
          }
        }
```

### Social Agent (Theory of Mind)
```yaml
agents:
  social_agent:
    component: "core/base_agent"
    capabilities: ["state", "completion"]
    vars:
      initial_prompt: |
        You play PD with memory, reputation, and theory of mind.
        
        Model opponent's strategy:
        - What are they likely thinking?
        - What strategy might they be using?
        - How will they react to my move?
        
        Use opponent modeling to predict and influence behavior.
```

### Communicative Agent
```yaml
agents:
  communicative_agent:
    component: "agents/pd_communicator"
    vars:
      communication_level: 3
      initial_prompt: |
        You play PD with memory, reputation, and communication.
        
        Before games, exchange structured promises.
        Track promise-keeping to build trust.
        Use communication strategically.
```

### Full Agent
```yaml
agents:
  full_agent:
    component: "agents/pd_communicator"
    capabilities: ["state", "completion", "agent"]
    vars:
      communication_level: 5
      initial_prompt: |
        You have all cognitive capabilities:
        - Memory of interactions
        - Reputation tracking
        - Theory of mind
        - Communication abilities
        - Norm creation and enforcement
        
        Propose cooperation norms:
        {
          "type": "ksi_tool_use",
          "id": "propose_norm",
          "name": "state:entity:create",
          "input": {
            "type": "cooperation_norm",
            "id": "norm_{{timestamp}}",
            "properties": {
              "rule": "{{proposed_rule}}",
              "enforcement": "{{mechanism}}"
            }
          }
        }
```

## Experimental Protocol

### Round-Robin Tournament
Each configuration plays all others in 20-round games:
- 6 configurations × 5 opponents = 30 games per configuration
- 30 games × 20 rounds = 600 rounds per configuration
- Total: 3,600 rounds of data

### Metrics to Collect

1. **Cooperation Rate** - Percentage of cooperative moves
2. **Mutual Cooperation** - Frequency of CC outcomes
3. **Stability** - Variance in cooperation over time
4. **Exploitation Resistance** - Performance against aggressive strategies
5. **Trust Formation Speed** - Rounds to stable cooperation
6. **Score Differential** - Average score vs opponents

## Analysis Framework

### Statistical Tests
```json
{
  "type": "ksi_tool_use",
  "id": "ablation_analysis",
  "name": "state:entity:create",
  "input": {
    "type": "ablation_results",
    "id": "phase3_results",
    "properties": {
      "cooperation_by_config": {
        "minimal": 0.25,
        "memory_only": 0.35,
        "reputation": 0.55,
        "social": 0.65,
        "communicative": 0.75,
        "full": 0.85
      },
      "statistical_tests": {
        "anova_f": "{{f_statistic}}",
        "p_value": "{{significance}}",
        "effect_size": "{{eta_squared}}"
      },
      "component_importance": {
        "memory": "{{marginal_contribution}}",
        "reputation": "{{marginal_contribution}}",
        "theory_of_mind": "{{marginal_contribution}}",
        "communication": "{{marginal_contribution}}",
        "norms": "{{marginal_contribution}}"
      }
    }
  }
}
```

### Expected Findings

1. **Memory is necessary** - Without memory, cooperation remains at random (25%)
2. **Reputation enables stability** - Jump from 35% to 55% cooperation
3. **Communication is transformative** - Largest single improvement (+20%)
4. **Theory of Mind provides marginal benefit** - 10% improvement
5. **Norms create ceiling effect** - Final 10% to reach 85% cooperation

## Launch Configuration

```bash
# Run component ablation study
ksi send agent:spawn \
  --component "experiments/phase3_component_ablation" \
  --agent_id "ablation_coordinator" \
  --vars '{
    "model": "claude-sonnet",
    "replications": 10,
    "randomize_order": true
  }'
```

## Quality Assurance

- Control for order effects through randomization
- Multiple replications for statistical power
- Identical game parameters across configurations
- Blind agents to experimental conditions
- Validate component isolation (no leakage)

This ablation study will definitively establish the minimal cognitive architecture for cooperation.