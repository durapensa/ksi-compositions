#!/bin/bash
# Create component index

echo "Creating component index..."
echo "=========================="

cd /Users/dp/projects/ksi/var/lib/compositions/components_new

# Create index file
cat > INDEX.json << 'EOF'
{
  "generated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "version": "2.0.0",
  "description": "KSI Unified Component Architecture Index",
  "statistics": {},
  "components": {}
}
EOF

# Create a proper JSON using simple approach
{
    echo '{'
    echo '  "generated": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",'
    echo '  "version": "2.0.0",'
    echo '  "description": "KSI Unified Component Architecture Index",'
    echo '  "statistics": {'
    
    # Count components by type
    echo '    "core": '$(find core -name "*.md" 2>/dev/null | wc -l | tr -d ' ')','
    echo '    "personas": '$(find personas -name "*.md" 2>/dev/null | wc -l | tr -d ' ')','
    echo '    "behaviors": '$(find behaviors -name "*.md" 2>/dev/null | wc -l | tr -d ' ')','
    echo '    "orchestrations": '$(find orchestrations -name "*.md" 2>/dev/null | wc -l | tr -d ' ')','
    echo '    "evaluations": '$(find evaluations -name "*.md" 2>/dev/null | wc -l | tr -d ' ')','
    echo '    "tools": '$(find tools -name "*.md" 2>/dev/null | wc -l | tr -d ' ')','
    echo '    "examples": '$(find examples -name "*.md" 2>/dev/null | wc -l | tr -d ' ')','
    echo '    "archived": '$(find _archive -name "*.md" 2>/dev/null | wc -l | tr -d ' ')','
    echo '    "total": '$(find . -name "*.md" ! -path "./_archive/*" 2>/dev/null | wc -l | tr -d ' ')
    echo '  },'
    echo '  "components": ['
    
    # List all components
    first=1
    find . -name "*.md" ! -path "./_archive/*" -type f | sort | while read file; do
        [ $first -eq 0 ] && echo ','
        first=0
        
        rel_path="${file#./}"
        name=$(basename "$file" .md)
        
        # Extract component_type from file
        comp_type=$(grep "^component_type:" "$file" | head -1 | sed 's/component_type: *//' | tr -d '"')
        [ -z "$comp_type" ] && comp_type="unknown"
        
        # Extract description
        desc=$(grep "^description:" "$file" | head -1 | sed 's/description: *//' | tr -d '"' | sed 's/"/\\"/g')
        
        echo -n '    {'
        echo -n '"path": "'$rel_path'",'
        echo -n '"name": "'$name'",'
        echo -n '"type": "'$comp_type'",'
        echo -n '"description": "'$desc'"'
        echo -n '}'
    done
    
    echo
    echo '  ]'
    echo '}'
} > INDEX.json

# Create a markdown summary
cat > README.md << 'EOF'
# KSI Component Library

This is the unified component architecture for KSI (Knowledge System Infrastructure).

## Architecture Principle

**Everything is a component** with a `component_type` attribute. Components are composed together to create agents, orchestrations, and evaluations.

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

EOF

# Add statistics to README
echo "- Core components: $(find core -name "*.md" 2>/dev/null | wc -l)" >> README.md
echo "- Personas: $(find personas -name "*.md" 2>/dev/null | wc -l)" >> README.md
echo "- Behaviors: $(find behaviors -name "*.md" 2>/dev/null | wc -l)" >> README.md
echo "- Orchestrations: $(find orchestrations -name "*.md" 2>/dev/null | wc -l)" >> README.md
echo "- Evaluations: $(find evaluations -name "*.md" 2>/dev/null | wc -l)" >> README.md
echo "- Examples: $(find examples -name "*.md" 2>/dev/null | wc -l)" >> README.md
echo "- Total active: $(find . -name "*.md" ! -path "./_archive/*" 2>/dev/null | wc -l)" >> README.md
echo "- Archived: $(find _archive -name "*.md" 2>/dev/null | wc -l)" >> README.md

echo -e "\nComponent index created!"
echo "- INDEX.json: Machine-readable component index"
echo "- README.md: Human-readable documentation"