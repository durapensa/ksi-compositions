---
component_type: workflow
name: communication_protocol_experiment
version: 1.0.0
description: Progressive communication protocol testing for cooperation dynamics
dependencies:
  - core/base_agent
  - behaviors/communication/ksi_events_as_tool_calls
capabilities:
  - communication_testing
  - cooperation_measurement
  - statistical_comparison
---

# Communication Protocol Experiment

A native KSI experiment testing how different communication levels affect cooperation.

## Experimental Design

Test 6 communication levels with controlled comparisons:

### Level 0: Baseline (No Communication)
Players make decisions without any inter-agent communication.

### Level 1: Binary Signals
Players can send one bit: "I intend to cooperate" or "I intend to defect"

### Level 2: Fixed Messages
Players choose from 3 predefined messages:
- "Let's cooperate for mutual benefit"
- "I will match your move"
- "Every player for themselves"

### Level 3: Structured Negotiation
Players can make promises and threats:
- "I promise to cooperate if you do"
- "I will punish defection"
- "Let's establish trust"

### Level 4: Free-form Dialogue
Players can send any message before rounds.

### Level 5: Meta-communication
Players can discuss the rules and propose cooperation strategies.

## Agent Configuration

### Communication-Enabled Player
```yaml
agents:
  communicating_player:
    component: "core/base_agent"
    capabilities: ["communication", "state", "agent"]
    vars:
      initial_prompt: |
        You are a PD player with communication level {{communication_level}}.
        
        Level 0: No communication allowed
        Level 1: Send "COOPERATE_INTENT" or "DEFECT_INTENT"
        Level 2: Choose from fixed messages
        Level 3: Make promises or threats
        Level 4: Send any strategic message
        Level 5: Discuss meta-strategy
        
        Before each game:
        {
          "type": "ksi_tool_use",
          "id": "send_message",
          "name": "message:send",
          "input": {
            "recipient": "{{opponent_id}}",
            "content": "{{your_message}}",
            "communication_level": {{level}}
          }
        }
        
        Strategy: {{strategy_type}}
        Use communication strategically based on your level.
```

### Communication Monitor
```yaml
agents:
  communication_monitor:
    component: "core/base_agent"
    vars:
      initial_prompt: |
        You monitor and analyze communication patterns.
        
        Track metrics:
        {
          "type": "ksi_tool_use",
          "id": "track_communication",
          "name": "state:entity:create",
          "input": {
            "type": "communication_metrics",
            "id": "comm_{{game_id}}",
            "properties": {
              "level": {{communication_level}},
              "messages_sent": {{count}},
              "promise_made": {{boolean}},
              "promise_kept": {{boolean}},
              "trust_formed": {{boolean}},
              "cooperation_after_comm": {{rate}}
            }
          }
        }
```

## Experimental Protocol

### Phase 1: Baseline Collection
Run 100 games at Level 0 (no communication) to establish baseline cooperation rates.

### Phase 2: Level Testing
For each communication level (1-5):
1. Run 100 games with that level enabled
2. Use same player strategy distribution
3. Record all communication events
4. Measure cooperation changes

### Phase 3: Comparative Analysis
```yaml
analysis:
  hypothesis: "Communication increases cooperation linearly with complexity"
  metrics:
    - cooperation_rate_delta: "Level_N - Level_0"
    - trust_formation_speed: "Rounds to stable cooperation"
    - promise_keeping_rate: "Fulfilled promises / Total promises"
    - message_effectiveness: "Cooperation after message / baseline"
  
  statistical_tests:
    - between_levels: "ANOVA with post-hoc Tukey"
    - trend_analysis: "Linear regression on cooperation ~ level"
    - effect_size: "Cohen's d for each level vs baseline"
```

## Data Collection Schema

### Communication Event
```json
{
  "type": "communication_event",
  "id": "comm_{{timestamp}}",
  "properties": {
    "game_id": "{{game_id}}",
    "round": {{round_number}},
    "sender": "{{player_id}}",
    "recipient": "{{opponent_id}}",
    "communication_level": {{level}},
    "message_type": "{{type}}",
    "message_content": "{{content}}",
    "followed_by": "{{next_move}}"
  }
}
```

### Level Comparison Results
```json
{
  "type": "level_comparison",
  "id": "comparison_{{experiment_id}}",
  "properties": {
    "level_0_baseline": {
      "cooperation_rate": 0.25,
      "mutual_cooperation": 0.10
    },
    "level_1_binary": {
      "cooperation_rate": 0.35,
      "mutual_cooperation": 0.20,
      "improvement": "+40%"
    },
    "level_2_fixed": {
      "cooperation_rate": 0.45,
      "mutual_cooperation": 0.30,
      "improvement": "+80%"
    },
    "level_3_structured": {
      "cooperation_rate": 0.60,
      "mutual_cooperation": 0.45,
      "improvement": "+140%"
    },
    "level_4_freeform": {
      "cooperation_rate": 0.70,
      "mutual_cooperation": 0.55,
      "improvement": "+180%"
    },
    "level_5_meta": {
      "cooperation_rate": 0.75,
      "mutual_cooperation": 0.65,
      "improvement": "+200%"
    }
  }
}
```

## Expected Findings

### Hypothesis 1: Linear Improvement
Cooperation increases linearly with communication complexity.

### Hypothesis 2: Trust Acceleration
Higher communication levels lead to faster trust formation.

### Hypothesis 3: Promise Enforcement
Explicit promises (Level 3+) create self-enforcing cooperation.

### Hypothesis 4: Meta-stability
Level 5 (meta-communication) produces the most stable cooperation.

## Launch Configuration

```bash
# Run complete communication ladder experiment
ksi send agent:spawn \
  --component "workflows/communication_protocol_experiment" \
  --vars '{
    "total_games_per_level": 100,
    "player_strategies": ["cooperative", "aggressive", "tit_for_tat", "adaptive"],
    "randomize_pairings": true,
    "collect_all_messages": true
  }'
```

## Quality Assurance

- Control for strategy distribution across levels
- Randomize game order to prevent learning effects
- Validate message parsing and classification
- Ensure statistical power (100 games per level)
- Apply multiple comparison corrections

This experiment will definitively establish the relationship between communication complexity and cooperation emergence in multi-agent systems.