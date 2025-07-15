# KSI Compositions Repository

This repository contains reusable compositions for the KSI (Knowledge Systems Integration) platform, including agent profiles, orchestration patterns, prompts, and reusable fragments.

## Repository Structure

```
ksi-compositions/
├── profiles/            # Agent profiles
│   ├── base/           # Foundation profiles
│   ├── agents/         # Specialized agent profiles
│   └── fragments/      # Reusable profile components
├── orchestrations/      # Orchestration patterns
├── prompts/            # Prompt library
├── fragments/          # Cross-cutting components
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

# Load a profile
with open('profiles/base/base_single_agent.yaml') as f:
    profile = yaml.safe_load(f)

# Use profile in your system
agent = create_agent(profile)
```

## Component Types

### Profiles
Agent profiles define the behavior, capabilities, and configuration of AI agents:
- **Base profiles**: Foundation profiles for different agent types
- **Specialized profiles**: Task-specific agent configurations
- **Dynamic profiles**: Runtime-generated agent configurations

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
name: component_name
type: profile|orchestration|prompt|fragment
version: 1.0.0
description: "Brief description of component"
author: "Your Name"
metadata:
  tags: [tag1, tag2]
  use_cases: [use_case1, use_case2]
# Component-specific content
```

### Testing

Components should be tested before submission:

```bash
# Validate YAML syntax
yamllint profiles/new_profile.yaml

# Test component loading
python -c "import yaml; print(yaml.safe_load(open('profiles/new_profile.yaml')))"
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