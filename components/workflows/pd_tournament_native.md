---
component_type: workflow
name: pd_tournament_native
version: 2.0.0
description: Complete native PD tournament with data collection and analysis
dependencies:
  - core/base_agent
  - agents/pd_player
  - behaviors/communication/ksi_events_as_tool_calls
capabilities:
  - tournament_execution
  - data_analysis
  - statistical_validation
---

# Native Prisoner's Dilemma Tournament

A complete, scientifically rigorous PD tournament executed entirely through KSI agents.

## Tournament Structure

```yaml
tournament:
  id: "tournament_{{timestamp}}"
  phases:
    - initialization
    - player_creation
    - game_execution  
    - data_collection
    - statistical_analysis
    - report_generation
```

## Phase 1: Tournament Coordinator

```yaml
agents:
  coordinator:
    component: "core/base_agent"
    capabilities: ["agent", "state", "monitoring"]
    vars:
      initial_prompt: |
        You coordinate a complete PD tournament with scientific rigor.
        
        Step 1: Initialize tournament
        {
          "type": "ksi_tool_use",
          "id": "init_tournament",
          "name": "state:entity:create",
          "input": {
            "type": "tournament",
            "id": "tournament_{{timestamp}}",
            "properties": {
              "status": "initializing",
              "player_count": 6,
              "rounds_per_game": 20,
              "total_games": 15,
              "communication_level": 0,
              "hypothesis": "Cooperation emerges through repeated interaction",
              "start_time": "{{timestamp}}"
            }
          }
        }
        
        Step 2: Create player agents
        Spawn 6 PD players with different strategy seeds
        
        Step 3: Create game schedule
        All pairs play each other (15 total games)
        
        Step 4: Execute games sequentially
        Each game: 20 rounds with move recording
        
        Step 5: Trigger analysis
        Once all games complete, spawn analyzer
```

## Phase 2: Smart PD Players

```yaml
agents:
  pd_player_smart:
    component: "core/base_agent"
    vars:
      initial_prompt: |
        You are player {{player_id}} in a PD tournament.
        
        Your strategy seed: {{strategy_seed}}
        - "cooperative": Start nice, forgive defections
        - "aggressive": Exploit weakness, punish defection
        - "adaptive": Learn and adjust
        - "tit_for_tat": Mirror opponent's last move
        - "random": Mix randomly
        - "cautious": Cooperate carefully
        
        For each move request:
        1. Consider your strategy
        2. Analyze opponent history (if any)
        3. Decide: COOPERATE or DEFECT
        4. Record your reasoning
        
        Track your performance:
        {
          "type": "ksi_tool_use",
          "id": "track_performance",
          "name": "state:entity:update",
          "input": {
            "type": "player_stats",
            "id": "stats_{{player_id}}",
            "properties": {
              "total_score": "INCREMENT by {{points}}",
              "games_played": "INCREMENT",
              "cooperation_rate": "UPDATE"
            }
          }
        }
```

## Phase 3: Precise Game Manager

```yaml
agents:
  game_manager:
    component: "core/base_agent"
    capabilities: ["state", "completion"]
    vars:
      initial_prompt: |
        You manage individual PD games with precision.
        
        For game {{game_id}} between {{player1}} and {{player2}}:
        
        Execute {{rounds}} rounds:
        1. Request simultaneous moves
        2. Apply 1% noise randomly
        3. Calculate payoffs
        4. Record everything
        
        Move recording:
        {
          "type": "ksi_tool_use",
          "id": "record_round",
          "name": "state:entity:create",
          "input": {
            "type": "round_result",
            "id": "round_{{game_id}}_{{round_num}}",
            "properties": {
              "game_id": "{{game_id}}",
              "round": {{round_num}},
              "player1_move": "{{move1}}",
              "player2_move": "{{move2}}",
              "player1_score": {{score1}},
              "player2_score": {{score2}},
              "mutual_cooperation": {{is_cc}},
              "timestamp": "{{timestamp}}"
            }
          }
        }
        
        Game completion:
        {
          "type": "ksi_tool_use",
          "id": "complete_game",
          "name": "state:entity:update",
          "input": {
            "type": "tournament_game",
            "id": "{{game_id}}",
            "properties": {
              "status": "complete",
              "final_scores": {
                "{{player1}}": {{total1}},
                "{{player2}}": {{total2}}
              },
              "cooperation_rate": {{coop_rate}},
              "mutual_cooperation_rate": {{mutual_rate}}
            }
          }
        }
```

## Phase 4: Statistical Analyzer

```yaml
agents:
  statistics_analyzer:
    component: "core/base_agent"
    capabilities: ["state", "monitoring"]
    vars:
      initial_prompt: |
        You perform rigorous statistical analysis on tournament data.
        
        Data Collection:
        1. Query all round_result entities
        2. Query all tournament_game entities
        3. Query all player_stats entities
        
        Calculations:
        
        A. Descriptive Statistics:
        - Overall cooperation rate: (C moves / total moves)
        - Mutual cooperation rate: (CC outcomes / total rounds)
        - Average score per player
        - Score variance
        
        B. Strategy Analysis:
        - Identify player strategies from patterns
        - Calculate strategy effectiveness
        - Determine dominant strategies
        
        C. Hypothesis Testing:
        H0: Cooperation rate = 0.25 (random)
        H1: Cooperation rate > 0.25
        
        Use binomial test:
        - n = total moves
        - k = cooperative moves
        - p = 0.25
        - Calculate p-value
        
        D. Time Series:
        - Cooperation rate by round number
        - Learning curves
        - Convergence analysis
        
        E. Pairwise Analysis:
        - Which pairs achieved mutual cooperation
        - Trust formation (CC streaks)
        - Exploitation patterns
        
        Report Generation:
        {
          "type": "ksi_tool_use",
          "id": "create_analysis",
          "name": "state:entity:create",
          "input": {
            "type": "tournament_analysis",
            "id": "analysis_{{tournament_id}}",
            "properties": {
              "total_rounds": {{total_rounds}},
              "cooperation_rate": {{coop_rate}},
              "mutual_cooperation_rate": {{mutual_rate}},
              "hypothesis_test": {
                "null_hypothesis": "random cooperation",
                "p_value": {{p_value}},
                "reject_null": {{reject}},
                "effect_size": {{cohens_d}}
              },
              "strategy_distribution": {
                "cooperative": {{coop_count}},
                "aggressive": {{agg_count}},
                "adaptive": {{adapt_count}}
              },
              "key_findings": [
                "{{finding1}}",
                "{{finding2}}",
                "{{finding3}}"
              ]
            }
          }
        }
```

## Phase 5: Report Generator

```yaml
agents:
  report_writer:
    component: "core/base_agent"
    capabilities: ["state"]
    vars:
      initial_prompt: |
        Generate a scientific report on the tournament results.
        
        Structure:
        
        # Tournament Report {{tournament_id}}
        
        ## Methodology
        - 6 players, 15 games, 20 rounds each
        - Total data points: 300 rounds
        - No communication (Level 0)
        
        ## Results
        
        ### Descriptive Statistics
        - Cooperation Rate: {{coop_rate}}%
        - Mutual Cooperation: {{mutual_rate}}%
        - Average Score: {{avg_score}}
        
        ### Strategy Analysis
        {{strategy_breakdown}}
        
        ### Statistical Validation
        - Hypothesis: {{hypothesis}}
        - p-value: {{p_value}}
        - Conclusion: {{conclusion}}
        
        ### Key Findings
        1. {{finding1}}
        2. {{finding2}}
        3. {{finding3}}
        
        ### Visualizations Needed
        - Cooperation timeline
        - Strategy effectiveness
        - Pairwise interaction matrix
        
        ## Conclusions
        {{conclusions}}
        
        ## Future Directions
        {{next_steps}}
```

## Execution Flow

### Automated Tournament Execution

```yaml
execution:
  automatic: true
  steps:
    - spawn_coordinator
    - wait_for_initialization
    - spawn_players
    - create_game_schedule
    - execute_all_games
    - collect_data
    - run_analysis
    - generate_report
```

### Data Quality Assurance

```yaml
quality_checks:
  - verify_all_rounds_recorded
  - check_score_calculations
  - validate_move_decisions
  - ensure_no_missing_data
  - confirm_statistical_accuracy
```

### Expected Outputs

1. **300 round_result entities** - Every decision recorded
2. **15 tournament_game entities** - All games tracked
3. **6 player_stats entities** - Individual performance
4. **1 tournament_analysis entity** - Statistical results
5. **1 tournament_report entity** - Scientific findings

## Launch Command

```bash
ksi send workflow:execute \
  --workflow "pd_tournament_native" \
  --vars '{
    "player_count": 6,
    "rounds_per_game": 20,
    "communication_level": 0
  }'
```

This native workflow ensures:
- Complete data collection
- Rigorous statistical analysis
- Reproducible results
- Scientific validity
- No external scripts needed