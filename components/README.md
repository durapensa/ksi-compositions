# KSI Component Library

This is the unified component architecture for KSI (Knowledge System Infrastructure).

## Architecture Principle

**Everything is a component** with a `type` attribute. Components are composed together to create agents, orchestrations, and evaluations.

## Directory Structure

```
components/
├── core/              # Essential building blocks
├── personas/          # Domain expertise & personalities  
├── behaviors/         # Reusable behavior mixins
├── orchestrations/    # Multi-agent coordination patterns
├── evaluations/       # Quality assessment components
├── tools/            # External integrations
├── examples/         # Learning examples
└── _archive/         # Legacy/test components
```

## Component Types

- **core**: Fundamental components (base_agent, json_emitter)
- **persona**: Domain expertise and personality definitions
- **behavior**: Reusable capabilities and mixins
- **orchestration**: Multi-agent workflow patterns
- **evaluation**: Quality metrics and test suites
- **tool**: External system integrations
- **example**: Demo and learning components

## Component Standard

All components use YAML frontmatter:

```yaml
---
component_type: persona
name: data_analyst
version: 2.0.0
description: Senior data analyst with statistical expertise
dependencies:
  - core/base_agent
  - behaviors/communication/mandatory_json
capabilities:
  - statistical_analysis
  - data_visualization
---
```

## Usage

Components are referenced by their path relative to the components directory:

```bash
# Spawn an agent from a persona
ksi send agent:spawn_from_component --component "personas/analysts/data_analyst"

# Use in orchestrations
agents:
  - id: analyst
    component: personas/analysts/data_analyst
```

## Statistics

- Core components:        2
- Personas:        7
- Behaviors:        2
- Orchestrations:        7
- Evaluations:        8
- Examples:        1
- Total active:       28
- Archived:       36
