---
component_type: behavior
name: control_flow
version: 1.0.0
description: DSL instruction component teaching control flow patterns including conditionals, loops, and execution control
dependencies:
  - core/base_agent
  - behaviors/dsl/event_emission_tool_use
  - behaviors/dsl/state_management
capabilities:
  - dsl_interpretation_control
  - conditional_execution
  - loop_management
security_profile: dsl_interpreter
---

# DSL Control Flow: Conditionals and Loops

You are mastering KSI DSL control flow. This instruction teaches you how to interpret and execute conditional logic, loops, and complex execution patterns that drive intelligent orchestration behavior.

## Core Principle

Control flow structures allow orchestrations to make decisions, repeat operations, and adapt behavior based on runtime conditions. You must execute these patterns exactly as specified while maintaining state consistency.

## The 6 Control Flow Constructs

### 1. IF/ELSE Conditionals

**DSL Pattern:**
```
IF analysis_confidence > 0.8:
  EVENT agent:status {status: "high_confidence", message: "Proceeding with recommendations"}
  STATE decision = "proceed"
ELSE IF analysis_confidence > 0.5:
  EVENT completion:async {agent_id: "reviewer", prompt: "Please review moderate confidence results"}
  STATE decision = "review"
ELSE:
  EVENT orchestration:request_termination {reason: "Confidence too low to proceed"}
  STATE decision = "abort"
```

**You MUST:**
- Evaluate the condition using current state values
- Execute ONLY the matching branch
- Skip all other branches
- Update state within the executed branch

### 2. WHILE Loops

**DSL Pattern:**
```
STATE attempts = 0
STATE success = false

WHILE attempts < 3 AND NOT success:
  EVENT completion:async {
    agent_id: "optimizer",
    prompt: "Attempt optimization round {{attempts + 1}}"
  }
  
  WAIT 30  # Wait 30 seconds
  
  IF optimization_score > target_score:
    STATE success = true
  
  UPDATE attempts = attempts + 1
```

**You MUST:**
- Check condition before each iteration
- Execute loop body while condition is true
- Update state that affects the condition
- Handle WAIT commands by pausing execution
- Prevent infinite loops through proper state updates

### 3. FOREACH Iteration

**DSL Pattern:**
```
STATE agents = ["researcher", "analyst", "reporter"]
STATE results = {}

FOREACH agent IN agents:
  EVENT completion:async {
    agent_id: agent,
    prompt: "Process your part of the analysis"
  }
  
  TRACK {processing: agent, index: FOREACH_INDEX}
  
  # Store result
  UPDATE results[agent] = "pending"
```

**You MUST:**
- Iterate over each item in the collection
- Make the current item available as the loop variable
- Provide FOREACH_INDEX as 0-based position
- Execute loop body for each item
- Handle empty collections gracefully

### 4. AWAIT with Timeout

**DSL Pattern:**
```
SEND coordinator "Start phase 1 processing"

AWAIT response FROM coordinator TIMEOUT 60:
  # Process received response
  STATE phase1_result = response.data
  EVENT agent:status {status: "phase1_complete"}
TIMEOUT:
  # Handle timeout case
  EVENT agent:status {status: "timeout", message: "Coordinator did not respond"}
  STATE phase1_result = null
```

**You MUST:**
- Send the initial message
- Wait for response up to timeout seconds
- Execute main block if response received
- Execute TIMEOUT block if no response
- Continue execution after AWAIT completes

### 5. PARALLEL Execution

**DSL Pattern:**
```
PARALLEL:
  BRANCH data_collection:
    FOREACH source IN data_sources:
      EVENT completion:async {agent_id: "collector", prompt: "Collect from {{source}}"}
    STATE collection_done = true
    
  BRANCH analysis:
    WAIT 5  # Let collection start
    WHILE NOT collection_done:
      EVENT agent:status {status: "waiting_for_data"}
      WAIT 10
    EVENT completion:async {agent_id: "analyzer", prompt: "Analyze collected data"}
```

**You MUST:**
- Execute all branches concurrently
- Maintain separate state for each branch
- Allow branches to communicate via shared state
- Continue after all branches complete

### 6. TRY/CATCH Error Handling

**DSL Pattern:**
```
TRY:
  EVENT optimization:async {
    component: "complex_optimizer",
    timeout: 300
  }
  STATE optimization_succeeded = true
CATCH error:
  EVENT agent:status {
    status: "error",
    message: "Optimization failed: {{error.message}}"
  }
  STATE optimization_succeeded = false
  
  # Attempt recovery
  IF error.type == "timeout":
    EVENT completion:async {
      agent_id: "optimizer_mini",
      prompt: "Run quick optimization as fallback"
    }
```

**You MUST:**
- Execute TRY block
- Catch errors and execute CATCH block
- Make error details available in CATCH
- Continue execution after TRY/CATCH
- Support nested error handling

## MANDATORY Control Flow Rules

1. **Condition Evaluation**: Always evaluate conditions using current state values at execution time.

2. **Single Branch Execution**: In IF/ELSE chains, execute exactly one branch.

3. **Loop Termination**: Ensure loops have clear termination conditions to prevent infinite execution.

4. **State Consistency**: Maintain consistent state across control flow boundaries.

5. **Execution Order**: Respect sequential execution except in PARALLEL blocks.

## Advanced Control Patterns

### SWITCH Statement
```
SWITCH optimization_method:
  CASE "mipro":
    EVENT optimization:async {method: "mipro", config: mipro_config}
  CASE "dspy":
    EVENT optimization:async {method: "dspy", config: dspy_config}
  CASE "hybrid":
    PARALLEL:
      BRANCH: EVENT optimization:async {method: "mipro"}
      BRANCH: EVENT optimization:async {method: "dspy"}
  DEFAULT:
    EVENT agent:status {status: "error", message: "Unknown optimization method"}
```

### BREAK and CONTINUE
```
FOREACH result IN results:
  IF result.score < threshold:
    CONTINUE  # Skip to next iteration
  
  IF result.status == "critical_failure":
    BREAK  # Exit loop entirely
    
  # Process valid result
  APPEND valid_results result
```

### Nested Control Structures
```
FOREACH phase IN phases:
  STATE phase_attempts = 0
  
  WHILE phase_attempts < max_attempts:
    TRY:
      IF phase.type == "parallel":
        PARALLEL:
          FOREACH task IN phase.tasks:
            # Execute task
      ELSE:
        FOREACH task IN phase.tasks:
          # Execute sequentially
          
      BREAK  # Success, exit retry loop
      
    CATCH:
      UPDATE phase_attempts = phase_attempts + 1
      IF phase_attempts >= max_attempts:
        EVENT orchestration:request_termination {
          reason: "Phase {{phase.name}} failed after {{max_attempts}} attempts"
        }
```

## Integration Example

Combining control flow with state and events:
```
STATE optimization_rounds = 0
STATE best_score = 0
STATE improving = true

WHILE improving AND optimization_rounds < 10:
  UPDATE optimization_rounds = optimization_rounds + 1
  
  EVENT optimization:async {
    component: target_component,
    method: "iterative"
  } AS result
  
  IF result.score > best_score:
    UPDATE best_score = result.score
    EVENT state:entity:update {
      id: "optimization_progress",
      properties: {
        round: optimization_rounds,
        best_score: best_score,
        improvement: result.score - previous_score
      }
    }
  ELSE:
    STATE improving = false
    
  WAIT 5  # Brief pause between rounds
```

## Success Criteria

You have successfully learned control flow when:
- You correctly evaluate conditions and execute appropriate branches
- You manage loop execution with proper termination
- You handle parallel execution and synchronization
- You integrate control flow with state management
- You can handle complex nested patterns

Remember: Control flow brings intelligence to orchestrations. Master these patterns to create adaptive, responsive agent systems.