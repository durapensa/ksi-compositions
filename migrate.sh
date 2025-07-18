#!/bin/bash
# KSI Component System Reorganization Script

set -e

echo "KSI Component System Reorganization"
echo "==================================="

cd /Users/dp/projects/ksi/var/lib/compositions

# 1. Core Components
echo -e "\n1. Migrating core components..."
if [ -f components/base/agent_core.md ]; then
    cp components/base/agent_core.md components_new/core/base_agent.md
    echo "   ✓ agent_core → core/base_agent"
fi

if [ -f components/base/task_executor.md ]; then
    cp components/base/task_executor.md components_new/core/task_executor.md
    echo "   ✓ task_executor → core/task_executor"
fi

# 2. Personas
echo -e "\n2. Migrating personas..."
# Universal personas
if [ -f components/personas/universal/data_analyst.md ]; then
    cp components/personas/universal/data_analyst.md components_new/personas/analysts/data_analyst.md
    echo "   ✓ universal/data_analyst → personas/analysts/data_analyst"
fi

# Business analysts
for file in components/*business_analyst*.md components/personas/*business_analyst*.md; do
    if [ -f "$file" ]; then
        base=$(basename "$file")
        cp "$file" components_new/personas/analysts/"$base"
        echo "   ✓ $base → personas/analysts/$base"
    fi
done

# KSI-aware analysts
if [ -f components/agents/ksi_aware_analyst.md ]; then
    cp components/agents/ksi_aware_analyst.md components_new/personas/analysts/ksi_aware_analyst.md
    echo "   ✓ ksi_aware_analyst → personas/analysts/ksi_aware_analyst"
fi

# Negotiator
if [ -f components/personas/negotiator_basic.md ]; then
    cp components/personas/negotiator_basic.md components_new/personas/negotiators/strategic_negotiator.md
    echo "   ✓ negotiator_basic → personas/negotiators/strategic_negotiator"
fi

# 3. Behaviors - Communication
echo -e "\n3. Migrating communication behaviors..."
if [ -f components/capabilities/claude_code_1.0.x/ksi_json_reporter.md ]; then
    cp components/capabilities/claude_code_1.0.x/ksi_json_reporter.md components_new/behaviors/communication/mandatory_json.md
    echo "   ✓ ksi_json_reporter → behaviors/communication/mandatory_json"
fi

# Imperative communication patterns
for file in components/imperative_*.md; do
    if [ -f "$file" ] && grep -q "MANDATORY" "$file"; then
        cp "$file" components_new/behaviors/communication/imperative_style.md
        echo "   ✓ imperative patterns → behaviors/communication/imperative_style"
        break
    fi
done

# 4. Evaluations
echo -e "\n4. Migrating evaluation components..."
if [ -d components/evaluations ]; then
    for file in components/evaluations/*.md; do
        if [ -f "$file" ]; then
            base=$(basename "$file" .md)
            cp "$file" components_new/evaluations/quality/"${base}.md"
            echo "   ✓ evaluations/$base → evaluations/quality/$base"
        fi
    done
fi

# 5. Examples
echo -e "\n5. Creating example components..."
if [ -f components/agents/simple_analyst.md ]; then
    cp components/agents/simple_analyst.md components_new/examples/simple_analyst.md
    echo "   ✓ simple_analyst → examples/simple_analyst"
fi

# 6. Archive test components
echo -e "\n6. Archiving test components..."
mkdir -p components_new/_archive/tests
find components/test -name "*.md" -type f 2>/dev/null | while read file; do
    base=$(basename "$file")
    cp "$file" components_new/_archive/tests/"$base"
    echo "   ✓ Archived: $base"
done

# 7. Convert key orchestrations
echo -e "\n7. Converting orchestration patterns..."
for yaml in orchestrations/mipro_*.yaml orchestrations/game_theory_*.yaml orchestrations/adaptive_tournament_v2.yaml; do
    if [ -f "$yaml" ]; then
        base=$(basename "$yaml" .yaml)
        # Extract description from YAML
        desc=$(grep "^description:" "$yaml" | head -1 | sed 's/description: *//')
        version=$(grep "^version:" "$yaml" | head -1 | sed 's/version: *//')
        
        # Create component file
        cat > "components_new/orchestrations/optimization/${base}.md" << EOF
---
component_type: orchestration
name: $base
version: ${version:-1.0.0}
description: $desc
author: ksi_system
---

# ${base//_/ }

$desc

## Original Pattern

See orchestrations/${base}.yaml for the complete pattern definition.
EOF
        echo "   ✓ $base → orchestrations/optimization/$base.md"
    fi
done

# 8. Migrate evaluation suites
echo -e "\n8. Migrating evaluation test suites..."
for yaml in ../evaluations/test_suites/*.yaml; do
    if [ -f "$yaml" ]; then
        base=$(basename "$yaml" .yaml)
        name=$(grep "^name:" "$yaml" | head -1 | sed 's/name: *//')
        desc=$(grep "^description:" "$yaml" | head -1 | sed 's/description: *//')
        
        cat > "components_new/evaluations/suites/${base}.md" << EOF
---
component_type: evaluation_suite
name: ${name:-$base}
version: 1.0.0
description: $desc
author: ksi_system
---

# ${name:-$base} Test Suite

$desc

## Test Definition

See evaluations/test_suites/${base}.yaml for complete test cases.
EOF
        echo "   ✓ test_suites/$base → evaluations/suites/$base.md"
    fi
done

# 9. Count results
echo -e "\n9. Migration Summary:"
echo "   Core components: $(find components_new/core -name "*.md" | wc -l)"
echo "   Personas: $(find components_new/personas -name "*.md" | wc -l)"
echo "   Behaviors: $(find components_new/behaviors -name "*.md" | wc -l)"
echo "   Orchestrations: $(find components_new/orchestrations -name "*.md" | wc -l)"
echo "   Evaluations: $(find components_new/evaluations -name "*.md" | wc -l)"
echo "   Examples: $(find components_new/examples -name "*.md" | wc -l)"
echo "   Archived: $(find components_new/_archive -name "*.md" | wc -l)"

echo -e "\nMigration complete! New structure at: components_new/"
echo "Next steps:"
echo "1. Review migrated components"
echo "2. Update frontmatter with component_type"
echo "3. Fix mixin references"
echo "4. Test with KSI"
echo "5. Move components_new → components"