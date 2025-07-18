# KSI Component System Reorganization Plan

## Core Principle: Everything is a Component

Every piece in KSI is a component with a `component_type` attribute. This creates a unified mental model where components are composed to create functionality.

## New Directory Structure

```
components/
├── core/                    # Essential building blocks
│   ├── base_agent.md       # Fundamental agent component
│   ├── json_emitter.md     # Core JSON emission behavior
│   ├── event_handler.md    # Event handling patterns
│   └── session_manager.md  # Session continuity
│
├── personas/               # Domain expertise & personalities
│   ├── analysts/          # Various analyst types
│   │   ├── data_analyst.md
│   │   ├── business_analyst.md
│   │   └── system_analyst.md
│   ├── developers/        # Development personas
│   │   ├── ksi_developer.md
│   │   └── optimization_engineer.md
│   ├── thinkers/          # Thinking style personas
│   │   ├── systematic_thinker.md
│   │   ├── creative_thinker.md
│   │   └── critical_thinker.md
│   └── negotiators/       # Game theory personas
│       └── strategic_negotiator.md
│
├── behaviors/             # Reusable behavior mixins
│   ├── communication/     # Communication patterns
│   │   ├── mandatory_json.md
│   │   ├── imperative_style.md
│   │   └── structured_output.md
│   ├── coordination/      # Multi-agent behaviors
│   │   ├── agent_spawning.md
│   │   ├── message_routing.md
│   │   └── state_tracking.md
│   └── integration/       # System integration
│       ├── ksi_awareness.md
│       └── tool_usage.md
│
├── orchestrations/        # Multi-agent coordination
│   ├── optimization/      # Optimization patterns
│   │   ├── mipro_framework.md
│   │   ├── bayesian_search.md
│   │   └── game_theory_optimization.md
│   ├── tournaments/       # Competition patterns
│   │   ├── adaptive_tournament.md
│   │   └── evolution_tournament.md
│   ├── workflows/         # Business workflows
│   │   ├── analysis_pipeline.md
│   │   └── review_process.md
│   └── research/          # Research patterns
│       ├── hypothesis_testing.md
│       └── iterative_refinement.md
│
├── evaluations/          # Assessment components
│   ├── quality/          # Quality metrics
│   │   ├── response_quality.md
│   │   ├── game_theory_metrics.md
│   │   └── cooperation_score.md
│   ├── judges/           # Evaluation personas
│   │   ├── quality_judge.md
│   │   └── fairness_judge.md
│   └── rubrics/          # Scoring rubrics
│       └── optimization_rubric.md
│
├── tools/                # External integrations
│   ├── mcp/              # MCP tool components
│   ├── git/              # Git integration
│   └── apis/             # API access patterns
│
└── examples/             # Learning examples
    ├── simple_agent.md
    ├── json_emitter_demo.md
    └── orchestration_demo.md
```

## Component Frontmatter Standard

```yaml
---
component_type: persona        # Required: persona|behavior|orchestration|evaluation|tool|core
name: data_analyst            # Required: Component identifier
version: 2.0.0               # Required: Semantic versioning
description: Senior data analyst with statistical expertise
author: ksi_system
created: 2025-01-18
tags: [analysis, statistics, business_intelligence]
dependencies:                 # Other components this needs
  - core/base_agent
  - behaviors/communication/mandatory_json
capabilities:                 # What this component provides
  - statistical_analysis
  - data_visualization
  - insight_generation
compatibility:
  models: [claude-sonnet, claude-opus]
  ksi_version: ">=2.0.0"
---
```

## Migration Categories

### 1. KEEP & REORGANIZE (High Quality Production Components)
- `personas/universal/data_analyst.md` → `personas/analysts/data_analyst.md`
- `components/base/agent_core.md` → `core/base_agent.md`
- `capabilities/claude_code_1.0.x/ksi_json_reporter.md` → `behaviors/communication/mandatory_json.md`
- All game theory evaluations → `evaluations/quality/`
- MIPRO orchestrations → `orchestrations/optimization/`

### 2. MERGE & CONSOLIDATE (Redundant Variations)
- Multiple "imperative_*" components → Single `behaviors/communication/imperative_style.md`
- Various analyst personas → Consolidated with clear differentiation
- Test variations (json_test_v1-v5) → Best practices in `behaviors/communication/mandatory_json.md`

### 3. ARCHIVE (Test/Experimental/Legacy)
- All test/* components → `_archive/tests/`
- Experimental JSON emission tests → `_archive/experiments/`
- Old orchestration patterns → `_archive/legacy/`
- Malformed/incomplete components → Remove entirely

### 4. DELETE (No Value)
- Empty or single-line files
- Duplicate test files
- Broken components with no content
- Pure test scaffolding

## Implementation Steps

1. **Create new directory structure**
2. **Migrate core components first** (establish foundation)
3. **Update component frontmatter** to new standard
4. **Fix all dependencies** (mixin references)
5. **Archive old components** 
6. **Update KSI daemon** to recognize new structure
7. **Rebuild component index**
8. **Test with key workflows**

## Benefits for Claude

1. **Clear mental model**: Everything is a component with a type
2. **Discoverable structure**: Organized by purpose, not implementation
3. **Reusable patterns**: Easy to find and compose behaviors
4. **Quality control**: Production components separated from experiments
5. **Version tracking**: Clear compatibility and dependencies

## Breaking Changes

1. All mixin paths will change
2. Component type attribute required
3. Directory structure completely different
4. Some components merged or removed
5. New dependency syntax

This is a one-time breaking change to establish a sustainable foundation.