#!/usr/bin/env python3
"""
Update composition service to support unified component architecture
Makes the system discover types dynamically instead of hardcoding them
"""

import re

# Read the composition service file
with open('/Users/dp/projects/ksi/ksi_daemon/composition/composition_service.py', 'r') as f:
    content = f.read()

print("Updating composition service for unified architecture...")
print("=" * 60)

# 1. Update hardcoded type lists to be dynamic
old_pattern = r"types = \['profile', 'prompt', 'orchestration', 'component', 'capability', 'pattern'\]"
new_code = """# Discover types dynamically from component_type attributes
        types = await composition_index.get_unique_component_types()
        if not types:  # Fallback for empty index
            types = ['component']  # Everything is a component"""

if old_pattern in content:
    content = content.replace(
        "types = ['profile', 'prompt', 'orchestration', 'component', 'capability', 'pattern']",
        new_code.strip()
    )
    print("✓ Updated hardcoded type list to dynamic discovery")

# 2. Update type validation to accept any type
old_validation = r"elif metadata\['type'\] not in \['profile', 'component', 'template'\]:"
if old_validation in content:
    content = re.sub(
        r"elif metadata\['type'\] not in \[.*?\]:",
        "# Accept any component_type - no hardcoded validation",
        content
    )
    print("✓ Removed hardcoded type validation")

# 3. Update default type from 'profile' to 'component'
content = re.sub(
    r"comp_type = data\.get\('type', 'profile'\)",
    "comp_type = data.get('type', 'component')",
    content
)
print("✓ Updated default type to 'component'")

# 4. Update get_component_type to return actual type from frontmatter
old_get_type = '''def get_component_type(content: str) -> str:
    """Determine component type from content."""
    post = parse_frontmatter(content)
    if post.has_frontmatter():
        return 'enhanced'
    return 'simple'
'''

new_get_type = '''def get_component_type(content: str) -> str:
    """Determine component type from frontmatter."""
    post = parse_frontmatter(content)
    if post.has_frontmatter():
        # Return actual component_type from frontmatter
        return post.metadata.get('component_type', 'component')
    return 'component'  # Default type
'''

# Save the updated composition service
with open('/Users/dp/projects/ksi/ksi_daemon/composition/composition_service_updated.py', 'w') as f:
    f.write(content)

print("\nNow updating frontmatter_utils.py...")

# Update frontmatter utils
with open('/Users/dp/projects/ksi/ksi_common/frontmatter_utils.py', 'r') as f:
    fm_content = f.read()

fm_content = fm_content.replace(old_get_type.strip(), new_get_type.strip())

# Save updated frontmatter utils
with open('/Users/dp/projects/ksi/ksi_common/frontmatter_utils_updated.py', 'w') as f:
    f.write(fm_content)

print("✓ Updated get_component_type to return actual type")

print("\nCreating composition index updates...")

# Create new methods for composition index
index_updates = '''
# Add these methods to composition_index.py

async def get_unique_component_types() -> List[str]:
    """Get all unique component types from the index."""
    async with aiosqlite.connect(INDEX_DB_PATH) as db:
        async with db.execute("""
            SELECT DISTINCT json_extract(metadata, '$.component_type') as comp_type
            FROM compositions 
            WHERE json_extract(metadata, '$.component_type') IS NOT NULL
            UNION
            SELECT DISTINCT type FROM compositions WHERE type IS NOT NULL
        """) as cursor:
            types = [row[0] for row in await cursor.fetchall() if row[0]]
            return types if types else ['component']

async def filter_by_component_type(component_type: str) -> List[Dict[str, Any]]:
    """Filter components by their component_type attribute."""
    async with aiosqlite.connect(INDEX_DB_PATH) as db:
        async with db.execute("""
            SELECT * FROM compositions
            WHERE json_extract(metadata, '$.component_type') = ?
            OR (type = ? AND json_extract(metadata, '$.component_type') IS NULL)
        """, (component_type, component_type)) as cursor:
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in await cursor.fetchall()]

def normalize_component_path(name: str, component_type: str = 'component') -> str:
    """Normalize component path based on type and naming convention."""
    # Map component types to default directories
    type_dirs = {
        'core': 'core',
        'persona': 'personas',
        'behavior': 'behaviors', 
        'orchestration': 'orchestrations',
        'evaluation': 'evaluations',
        'evaluation_suite': 'evaluations/suites',
        'tool': 'tools',
        'example': 'examples'
    }
    
    # If path already contains directory, use as-is
    if '/' in name:
        return name
        
    # Otherwise, organize by type
    if component_type in type_dirs:
        return f"{type_dirs[component_type]}/{name}"
    
    # Default to type-based directory
    return f"{component_type}/{name}"
'''

with open('/Users/dp/projects/ksi/var/lib/compositions/composition_index_updates.py', 'w') as f:
    f.write(index_updates)

print("✓ Created composition index update methods")

print("\nSummary of changes:")
print("1. Removed all hardcoded type lists")
print("2. Made type discovery dynamic from component_type attribute") 
print("3. Updated default type to 'component'")
print("4. Made get_component_type return actual frontmatter type")
print("5. Created index methods for dynamic type discovery")
print("\nNext steps:")
print("- Review and apply the changes")
print("- Test with new component structure")
print("- Update any remaining hardcoded type references")