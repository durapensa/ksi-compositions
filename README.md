# KSI Compositions Repository

This repository contains reusable compositions for the KSI (Knowledge Systems Integration) platform, including components, orchestration patterns, prompts, and capabilities.

## Repository Structure

```
ksi-compositions/
├── components/          # Unified component system
│   ├── core/           # Essential building blocks
│   ├── personas/       # Domain expertise & personalities
│   ├── behaviors/      # Reusable mixins
│   ├── evaluations/    # Quality assessments
│   ├── tools/          # External integrations
│   └── examples/       # Example components
├── orchestrations/      # Orchestration patterns
├── prompts/            # Prompt library
├── capabilities/       # System capabilities
├── patterns/           # Messaging and hierarchy patterns
└── schemas/            # Validation schemas
```

## Usage

### In KSI Systems

This repository is designed to be used as a git submodule in KSI systems:

```bash
git submodule add https://github.com/ksi-project/ksi-compositions.git var/lib/compositions
```

### Standalone Usage

Components can be used independently in any system that supports YAML-based configuration:

```python
import yaml

# Load a component
with open('components/core/base_agent.md') as f:
    component = f.read()

# Parse frontmatter and content
# Use component in your system
agent = create_agent(component)
```

## Component Types

### Components
The unified component system includes:
- **Core**: Essential building blocks (base_agent, multi_agent, etc.)
- **Personas**: Domain expertise & personalities (analysts, developers, thinkers)
- **Behaviors**: Reusable mixins (communication, coordination, integration)
- **Evaluations**: Quality assessments (judges, metrics, test suites)
- **Tools**: External integrations (MCP, Git, APIs)

### Orchestrations
Orchestration patterns define multi-agent workflows and coordination:
- **Debate patterns**: Adversarial discussion formats
- **Collaboration patterns**: Cooperative work arrangements
- **Tournament patterns**: Competitive evaluation formats

### Prompts
Reusable prompt templates organized by category:
- **Core prompts**: Fundamental system prompts
- **Specialized prompts**: Task-specific prompt templates
- **Conversation prompts**: Dialogue and interaction patterns

### Fragments
Modular components that can be mixed into other compositions:
- **Capabilities**: Specific capability definitions
- **Patterns**: Behavioral patterns and rules
- **Injections**: Runtime behavior modifications

## Contributing

### Adding New Components

1. **Create component file** in appropriate directory
2. **Follow naming conventions**: `snake_case.yaml`
3. **Include metadata**: name, version, description, author
4. **Add validation**: Ensure component follows schemas
5. **Update documentation**: Add to relevant README sections

### Component Format

All components should follow this structure:

```yaml
---
type: persona  # Required: core|persona|behavior|orchestration|evaluation|tool
name: component_name
version: 1.0.0
description: "Brief description of component"
author: "Your Name"
dependencies:
  - core/base_agent
capabilities:
  - capability_name
---
# Component content in Markdown
```

### Testing

Components should be tested before submission:

```bash
# Validate component structure
ksi send composition:validate_component --component "components/personas/my_persona.md"

# Test component loading
ksi send agent:spawn_from_component --component "components/personas/my_persona" --agent-id "test_agent"
```

## License

This repository is licensed under the MIT License. See LICENSE file for details.

## Community

- **Issues**: Report bugs and request features via GitHub issues
- **Discussions**: Join discussions about component design and usage
- **Contributions**: Submit pull requests for new components and improvements

## Compatibility

Components in this repository are designed to be compatible with:
- KSI v1.0+ systems
- Any YAML-based configuration system
- Standard AI orchestration platforms

## Changelog

See CHANGELOG.md for version history and changes.