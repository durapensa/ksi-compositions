
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
