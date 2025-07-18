#!/usr/bin/env python3
"""
KSI Component System Reorganization Script
Migrates to "everything is a component" model
"""

import os
import re
import yaml
import shutil
from pathlib import Path
from datetime import datetime
import json

# Base paths
COMPOSITIONS_DIR = Path("/Users/dp/projects/ksi/var/lib/compositions")
OLD_COMPONENTS = COMPOSITIONS_DIR / "components"
NEW_COMPONENTS = COMPOSITIONS_DIR / "components_new"
ARCHIVE_DIR = COMPOSITIONS_DIR / "_archive"

# Component mappings
MIGRATIONS = {
    # Core components
    "components/base/agent_core.md": {
        "dest": "core/base_agent.md",
        "type": "core",
        "updates": {"name": "base_agent", "component_type": "core"}
    },
    "components/base/task_executor.md": {
        "dest": "core/task_executor.md", 
        "type": "core",
        "updates": {"component_type": "core"}
    },
    
    # Personas - Analysts
    "components/personas/universal/data_analyst.md": {
        "dest": "personas/analysts/data_analyst.md",
        "type": "persona",
        "updates": {"component_type": "persona", "version": "2.0.0"}
    },
    "components/personas/business_analyst.md": {
        "dest": "personas/analysts/business_analyst.md",
        "type": "persona", 
        "updates": {"component_type": "persona"}
    },
    "components/agents/ksi_aware_analyst.md": {
        "dest": "personas/analysts/ksi_aware_analyst.md",
        "type": "persona",
        "updates": {"component_type": "persona"}
    },
    
    # Personas - Thinkers
    "components/personas/negotiator_basic.md": {
        "dest": "personas/negotiators/strategic_negotiator.md",
        "type": "persona",
        "updates": {"component_type": "persona", "name": "strategic_negotiator"}
    },
    
    # Behaviors - Communication
    "components/capabilities/claude_code_1.0.x/ksi_json_reporter.md": {
        "dest": "behaviors/communication/mandatory_json.md",
        "type": "behavior",
        "updates": {"component_type": "behavior", "name": "mandatory_json"}
    },
    "components/imperative_ksi_communication.md": {
        "dest": "behaviors/communication/imperative_style.md",
        "type": "behavior",
        "updates": {"component_type": "behavior", "name": "imperative_style"}
    },
    
    # Behaviors - Integration  
    "components/agents/simple_analyst.md": {
        "dest": "examples/simple_analyst.md",
        "type": "example",
        "updates": {"component_type": "example"}
    },
    
    # Evaluations
    "components/evaluations/game_theory_quality.md": {
        "dest": "evaluations/quality/game_theory_metrics.md",
        "type": "evaluation",
        "updates": {"component_type": "evaluation", "name": "game_theory_metrics"}
    },
    "components/evaluations/cooperation_quality.md": {
        "dest": "evaluations/quality/cooperation_score.md",
        "type": "evaluation",
        "updates": {"component_type": "evaluation", "name": "cooperation_score"}
    },
}

# Patterns to archive
ARCHIVE_PATTERNS = [
    r"test/.*\.md$",
    r"test_.*\.md$",
    r"imperative_(original|start|with_must|without_mandatory)\.md$",
    r"validation/.*\.md$",
    r"stress_test/.*\.md$",
    r"phase[0-9]/.*\.md$",
]

# Patterns to delete
DELETE_PATTERNS = [
    r"\.py$",  # Python files don't belong here
    r"^-$",    # Single dash files
]

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content"""
    if content.startswith('---\n'):
        try:
            _, fm, body = content.split('---\n', 2)
            return yaml.safe_load(fm), body
        except:
            pass
    return {}, content

def update_frontmatter(content, updates):
    """Update frontmatter with new fields"""
    fm, body = parse_frontmatter(content)
    
    # Apply updates
    fm.update(updates)
    
    # Ensure required fields
    if 'version' not in fm:
        fm['version'] = '1.0.0'
    if 'author' not in fm:
        fm['author'] = 'ksi_system'
    if 'created' not in fm:
        fm['created'] = datetime.now().strftime('%Y-%m-%d')
    
    # Format frontmatter
    fm_str = yaml.dump(fm, default_flow_style=False, sort_keys=False)
    return f"---\n{fm_str}---\n{body}"

def should_archive(path):
    """Check if file should be archived"""
    path_str = str(path)
    for pattern in ARCHIVE_PATTERNS:
        if re.search(pattern, path_str):
            return True
    return False

def should_delete(path):
    """Check if file should be deleted"""
    path_str = str(path)
    content = path.read_text()
    
    # Check patterns
    for pattern in DELETE_PATTERNS:
        if re.search(pattern, path_str):
            return True
    
    # Check for empty/worthless content
    if len(content.strip()) < 10:
        return True
    if content.strip() == '-':
        return True
        
    return False

def migrate_component(src_path, dest_path, updates):
    """Migrate a single component"""
    print(f"Migrating: {src_path} -> {dest_path}")
    
    # Read content
    content = (COMPOSITIONS_DIR / src_path).read_text()
    
    # Update frontmatter
    content = update_frontmatter(content, updates)
    
    # Update mixin paths
    content = update_mixin_references(content)
    
    # Create destination directory
    dest_full = NEW_COMPONENTS / dest_path
    dest_full.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    dest_full.write_text(content)

def update_mixin_references(content):
    """Update mixin references to new paths"""
    replacements = {
        "components/agent_instructions/": "behaviors/communication/",
        "components/capabilities/claude_code_1.0.x/": "behaviors/communication/",
        "components/base/": "core/",
        "components/personas/": "personas/",
        "components/agents/": "personas/analysts/",
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    return content

def archive_component(src_path):
    """Archive a component"""
    rel_path = src_path.relative_to(OLD_COMPONENTS)
    if 'test' in str(rel_path):
        dest = ARCHIVE_DIR / "tests" / rel_path.name
    else:
        dest = ARCHIVE_DIR / "legacy" / rel_path
    
    print(f"Archiving: {rel_path} -> {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest)

def main():
    """Execute the migration"""
    print("KSI Component System Reorganization")
    print("===================================")
    
    # Create new structure
    print("\n1. Creating new directory structure...")
    for dir_path in [
        "core", "personas/analysts", "personas/developers", "personas/thinkers",
        "personas/negotiators", "behaviors/communication", "behaviors/coordination",
        "behaviors/integration", "orchestrations/optimization", "orchestrations/tournaments",
        "orchestrations/workflows", "orchestrations/research", "evaluations/quality",
        "evaluations/judges", "evaluations/rubrics", "tools/mcp", "tools/git",
        "tools/apis", "examples", "_archive/tests", "_archive/legacy", "_archive/experiments"
    ]:
        (NEW_COMPONENTS / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Process migrations
    print("\n2. Migrating production components...")
    for src, config in MIGRATIONS.items():
        if (COMPOSITIONS_DIR / src).exists():
            migrate_component(src, config["dest"], config["updates"])
    
    # Process remaining components
    print("\n3. Processing remaining components...")
    for comp_path in OLD_COMPONENTS.rglob("*.md"):
        rel_path = comp_path.relative_to(COMPOSITIONS_DIR)
        
        # Skip if already migrated
        if str(rel_path) in MIGRATIONS:
            continue
            
        # Delete worthless files
        if should_delete(comp_path):
            print(f"Deleting: {rel_path}")
            continue
            
        # Archive test/experimental
        if should_archive(rel_path):
            archive_component(comp_path)
        else:
            # Unmapped production component - needs manual review
            print(f"NEEDS REVIEW: {rel_path}")
    
    # Migrate orchestrations
    print("\n4. Migrating orchestration patterns...")
    orch_mappings = {
        "mipro_bayesian_optimization.yaml": "orchestrations/optimization/mipro_bayesian.md",
        "mipro_game_theory_optimization.yaml": "orchestrations/optimization/mipro_game_theory.md",
        "game_theory_orchestration_v2.yaml": "orchestrations/workflows/game_theory_workflow.md",
        "adaptive_tournament_v2.yaml": "orchestrations/tournaments/adaptive_tournament.md",
    }
    
    for src, dest in orch_mappings.items():
        src_path = COMPOSITIONS_DIR / "orchestrations" / src
        if src_path.exists():
            # Convert YAML to component format
            data = yaml.safe_load(src_path.read_text())
            
            # Create component with frontmatter
            fm = {
                "component_type": "orchestration",
                "name": dest.split('/')[-1].replace('.md', ''),
                "version": data.get('version', '1.0.0'),
                "description": data.get('description', ''),
                "author": data.get('author', 'ksi_system'),
            }
            
            content = f"""---
{yaml.dump(fm, default_flow_style=False, sort_keys=False)}---

# {fm['name'].replace('_', ' ').title()}

{data.get('description', '')}

## Original Orchestration Data

```yaml
{yaml.dump(data, default_flow_style=False)}
```
"""
            
            dest_path = NEW_COMPONENTS / dest
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            dest_path.write_text(content)
            print(f"Migrated orchestration: {src} -> {dest}")
    
    print("\n5. Creating index file...")
    # Create component index
    index = {"components": {}, "stats": {}}
    
    for comp_path in NEW_COMPONENTS.rglob("*.md"):
        if '_archive' in str(comp_path):
            continue
            
        rel_path = comp_path.relative_to(NEW_COMPONENTS)
        content = comp_path.read_text()
        fm, _ = parse_frontmatter(content)
        
        comp_type = fm.get('component_type', 'unknown')
        index["components"][str(rel_path)] = {
            "type": comp_type,
            "name": fm.get('name', rel_path.stem),
            "version": fm.get('version', '1.0.0'),
            "description": fm.get('description', ''),
        }
        
        # Update stats
        if comp_type not in index["stats"]:
            index["stats"][comp_type] = 0
        index["stats"][comp_type] += 1
    
    # Write index
    with open(NEW_COMPONENTS / "INDEX.json", 'w') as f:
        json.dump(index, f, indent=2)
    
    print("\nMigration Summary:")
    print("==================")
    for comp_type, count in sorted(index["stats"].items()):
        print(f"{comp_type}: {count} components")
    
    print(f"\nTotal: {sum(index['stats'].values())} components")
    print(f"\nNew structure created at: {NEW_COMPONENTS}")
    print("\nNext steps:")
    print("1. Review components marked 'NEEDS REVIEW'")
    print("2. Test the new structure")
    print("3. Update KSI daemon code")
    print("4. Move components_new -> components")

if __name__ == "__main__":
    main()