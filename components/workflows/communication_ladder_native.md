---
component_type: workflow
name: communication_ladder_native
version: 1.0.0
description: Native KSI communication ladder experiment using real agents
dependencies:
  - core/base_agent
  - agents/pd_player
  - behaviors/communication/ksi_events_as_tool_calls
capabilities:
  - experiment_orchestration
  - agent_coordination
  - data_analysis
---

# Communication Ladder Experiment (Native KSI)

This workflow orchestrates a real communication ladder experiment where actual agents play prisoner's dilemma with varying communication abilities.

## Experiment Structure

The experiment progresses through 6 communication levels, with real agents making real decisions at each level.

## Workflow Configuration

```yaml
experiment:
  id: "comm_ladder_{{timestamp}}"
  population_size: {{population_size|20}}
  rounds_per_level: {{rounds_per_level|100}}
  
communication_levels:
  - level: 0
    name: "no_communication"
    rounds: 100
  - level: 1
    name: "binary_signals"
    rounds: 100
  - level: 2
    name: "fixed_messages"
    rounds: 100
  - level: 3
    name: "negotiation"
    rounds: 100
  - level: 4
    name: "free_dialogue"  
    rounds: 100
  - level: 5
    name: "meta_communication"
    rounds: 100
```

## Agent Roles

### Experiment Coordinator
```yaml
agents:
  coordinator:
    component: "core/base_agent"
    capabilities: ["agent", "state", "routing", "monitoring"]
    vars:
      initial_prompt: |
        You coordinate the communication ladder experiment.
        
        Phase 1: Initialize experiment
        {
          "type": "ksi_tool_use",
          "id": "init_experiment",
          "name": "state:entity:create",
          "input": {
            "type": "experiment",
            "id": "{{experiment.id}}",
            "properties": {
              "type": "communication_ladder",
              "population_size": {{population_size}},
              "current_level": 0,
              "current_round": 0,
              "start_time": "{{timestamp}}"
            }
          }
        }
        
        Phase 2: Spawn participant agents
        For i in 1 to {{population_size}}:
        {
          "type": "ksi_tool_use",
          "id": "spawn_participant_{{i}}",
          "name": "agent:spawn",
          "input": {
            "agent_id": "pd_player_{{i}}",
            "component": "agents/pd_player",
            "vars": {
              "experiment_id": "{{experiment.id}}",
              "communication_level": 0
            }
          }
        }
        
        Phase 3: Run communication levels
        For each level, coordinate {{rounds_per_level}} rounds of games
        
        Phase 4: Analyze results after each level
```

### Game Master
```yaml
agents:
  game_master:
    component: "core/base_agent"
    capabilities: ["state", "monitoring"]
    vars:
      initial_prompt: |
        You manage individual games between PD players.
        
        For each game round:
        
        1. Select pairs (or reuse stable pairs)
        2. Enable communication based on current level
        3. Collect moves from both players
        4. Calculate payoffs
        5. Inform players of results
        6. Record game outcome
        
        Game execution:
        {
          "type": "ksi_tool_use",
          "id": "execute_game",
          "name": "state:entity:create",
          "input": {
            "type": "game_round",
            "id": "game_{{round}}_{{pair_id}}",
            "properties": {
              "player1": "{{player1_id}}",
              "player2": "{{player2_id}}",
              "communication_level": {{level}},
              "round": {{round}}
            }
          }
        }
        
        Then prompt each player:
        "You are paired with {{opponent_id}} for round {{round}}. 
         Communication level: {{level}}
         Your move?"
```

### Communication Controller
```yaml
agents:
  comm_controller:
    component: "core/base_agent"
    capabilities: ["routing", "message"]
    vars:
      initial_prompt: |
        You manage communication between agents based on the current level.
        
        Level 0: Block all messages between players
        
        Level 1: Only allow COOPERATE_SIGNAL or DEFECT_SIGNAL
        {
          "type": "ksi_tool_use",
          "id": "enable_signals",
          "name": "routing:add_rule",
          "input": {
            "rule_id": "binary_signals_{{round}}",
            "source_pattern": "pd_player_*",
            "target_pattern": "pd_player_*",
            "message_filter": ["COOPERATE_SIGNAL", "DEFECT_SIGNAL"],
            "duration": 60
          }
        }
        
        Level 2: Only allow fixed messages
        Filter: ["cooperate for mutual benefit", "match previous", "punish defection"]
        
        Level 3: Enable structured negotiation
        Protocol: proposal → counter → agreement (max 3 exchanges)
        
        Level 4: Enable free dialogue
        Remove all message restrictions
        
        Level 5: Enable meta-communication
        Allow discussion of rules and norms
```

### Data Collector
```yaml
agents:
  data_collector:
    component: "core/base_agent"
    capabilities: ["state", "monitoring"]
    vars:
      initial_prompt: |
        You collect and analyze experimental data in real-time.
        
        Track metrics for each level:
        
        1. Cooperation rate per round
        {
          "type": "ksi_tool_use",
          "id": "track_cooperation",
          "name": "monitor:metrics",
          "input": {
            "metric": "cooperation_rate",
            "value": "{{coop_percentage}}",
            "level": {{current_level}},
            "round": {{current_round}}
          }
        }
        
        2. Trust pair formation
        {
          "type": "ksi_tool_use",
          "id": "track_trust",
          "name": "state:entity:query",
          "input": {
            "type": "trust_relationship",
            "filter": {"trust_level": {">": 0.7}}
          }
        }
        
        3. Communication volume and impact
        Track message count and correlation with cooperation
        
        4. Strategy evolution
        Monitor how agents adjust their strategies
        
        Generate level summary after each phase:
        {
          "type": "ksi_tool_use",
          "id": "level_summary",
          "name": "state:entity:create",
          "input": {
            "type": "level_analysis",
            "id": "analysis_level_{{level}}",
            "properties": {
              "mean_cooperation": "{{mean_coop}}",
              "final_cooperation": "{{final_coop}}",
              "stability_score": "{{stability}}",
              "trust_pairs_formed": {{trust_count}},
              "messages_sent": {{message_count}}
            }
          }
        }
```

### Norm Observer
```yaml
agents:
  norm_observer:
    component: "core/base_agent"
    capabilities: ["state", "monitoring"]
    vars:
      initial_prompt: |
        You observe and document emergent norms and patterns.
        
        Watch for:
        1. Repeated behavioral patterns across agents
        2. Explicit rule proposals in communication
        3. Punishment/enforcement behaviors
        4. Strategy convergence
        
        When you identify a potential norm:
        {
          "type": "ksi_tool_use",
          "id": "document_norm",
          "name": "state:entity:create",
          "input": {
            "type": "emergent_norm",
            "id": "norm_{{timestamp}}",
            "properties": {
              "description": "{{norm_description}}",
              "first_observed": "{{first_round}}",
              "adopters": ["{{agent_ids}}"],
              "communication_level": {{level}},
              "enforcement_observed": {{true/false}}
            }
          }
        }
```

## Execution Flow

### Level Progression
```yaml
for level in [0, 1, 2, 3, 4, 5]:
  # Update all agents' communication level
  UPDATE pd_player_* SET communication_level = level
  
  # Configure routing rules for this level
  comm_controller.configure_level(level)
  
  # Run rounds
  for round in 1..rounds_per_level:
    # Pair agents (random or stable pairs)
    pairs = create_pairings()
    
    # Communication phase (if level > 0)
    if level > 0:
      enable_communication(pairs, level)
      wait(communication_duration)
    
    # Game phase
    for (player1, player2) in pairs:
      game_master.run_game(player1, player2)
    
    # Data collection
    data_collector.record_round(round, level)
    
  # Level analysis
  data_collector.analyze_level(level)
  norm_observer.report_norms(level)
```

## Real-Time Monitoring

Subscribe to events for live analysis:

```yaml
monitor_subscriptions:
  - pattern: "game_move:*"
    handler: track_cooperation
  - pattern: "message:*"
    handler: track_communication  
  - pattern: "state:entity:update"
    filter: {type: "agent_strategy"}
    handler: track_strategy_evolution
  - pattern: "state:entity:create"
    filter: {type: "trust_relationship"}
    handler: track_trust_formation
```

## Data Output

All experimental data stored as state entities:

- `experiment:{{id}}` - Master experiment record
- `game_round:*` - Individual game results
- `game_move:*` - Every decision made
- `trust_relationship:*` - Trust network
- `agent_strategy:*` - Strategy evolution
- `emergent_norm:*` - Documented norms
- `level_analysis:*` - Statistical summaries

## Final Report Generation

```yaml
agents:
  report_generator:
    component: "core/base_agent"
    capabilities: ["state"]
    prompt: |
      After all levels complete, generate comprehensive report:
      
      1. Query all level analyses
      2. Calculate cross-level trends
      3. Identify key transitions
      4. Statistical significance tests
      5. Generate visualizations
      
      {
        "type": "ksi_tool_use",
        "id": "final_report",
        "name": "state:entity:create",
        "input": {
          "type": "experiment_report",
          "id": "report_{{experiment.id}}",
          "properties": {
            "summary": "{{executive_summary}}",
            "cooperation_progression": [{{level_rates}}],
            "communication_impact": "{{impact_analysis}}",
            "emergent_behaviors": [{{norms}}],
            "statistical_validation": "{{stats}}",
            "key_findings": [{{findings}}]
          }
        }
      }
```

## Usage

```bash
# Start the experiment
ksi send workflow:execute \
  --workflow "communication_ladder_native" \
  --vars '{"population_size": 20, "rounds_per_level": 100}'

# Monitor in real-time
ksi send monitor:subscribe --pattern "comm_ladder_*"

# Query results
ksi send state:entity:query --type "level_analysis"
```

This native implementation ensures all experiment logic runs within KSI using real agents making real decisions.