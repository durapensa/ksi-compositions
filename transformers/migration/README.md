# KSI Event Handler Migration Infrastructure

This directory contains templates, tools, and validation schemas for migrating Python event handlers to declarative YAML transformers.

## Directory Structure

```
migration/
├── templates/                    # Transformer pattern templates
│   ├── simple_forwarder.yaml    # Basic event forwarding patterns
│   ├── field_mapper.yaml        # Data restructuring patterns
│   ├── conditional_router.yaml  # If/else routing patterns
│   └── multi_target.yaml        # Multiple destination patterns
├── validation/                   # Validation schemas and rules
│   └── transformer_schemas.yaml # JSON schemas for validation
├── migration_tools/              # Analysis and migration utilities
│   └── handler_analyzer.py      # Handler analysis tool
└── README.md                     # This file
```

## Migration Templates

### simple_forwarder.yaml
Use for handlers that just forward events with minimal transformation:
- Pass-through data with `{{$}}`
- Simple field extraction
- Status propagation patterns

**Example Usage:**
```python
# BEFORE: Python handler
@event_handler("agent:spawned")
async def forward_to_monitor(data, context):
    await emit_event("monitor:agent_created", data)
```

```yaml
# AFTER: Simple forwarder transformer
transformers:
  - source: "agent:spawned"
    target: "monitor:agent_created"
    mapping: "{{$}}"
```

### field_mapper.yaml
Use for handlers that restructure and map event data:
- Extract specific fields
- Add computed values
- Create nested structures
- Entity lifecycle mapping

**Example Usage:**
```python
# BEFORE: Field mapping handler
@event_handler("agent:created")
async def map_to_state(data, context):
    await emit_event("state:entity:create", {
        "type": "agent",
        "id": data["agent_id"],
        "properties": {
            "name": data.get("name"),
            "created_at": timestamp_utc()
        }
    })
```

```yaml
# AFTER: Field mapper transformer
transformers:
  - source: "agent:created"
    target: "state:entity:create"
    mapping:
      type: "agent"
      id: "{{agent_id}}"
      properties:
        name: "{{name|display_name}}"
        created_at: "{{timestamp_utc()}}"
```

### conditional_router.yaml
Use for handlers with if/else logic for routing:
- Success/error routing
- Multi-condition routing
- Threshold-based routing

**Example Usage:**
```python
# BEFORE: Conditional handler
@event_handler("completion:result")
async def route_completion(data, context):
    if data.get("status") == "error":
        await emit_event("alert:completion_error", data)
    else:
        await emit_event("monitor:completion_success", data)
```

```yaml
# AFTER: Conditional router transformers
transformers:
  - source: "completion:result"
    condition: "status == 'error'"
    target: "alert:completion_error"
    mapping: "{{$}}"
    
  - source: "completion:result"
    condition: "status != 'error'"
    target: "monitor:completion_success"
    mapping: "{{$}}"
```

### multi_target.yaml
Use for handlers that emit to multiple targets:
- System lifecycle events
- State synchronization
- Error propagation to multiple systems

**Example Usage:**
```python
# BEFORE: Multi-target handler
@event_handler("agent:spawned")
async def notify_systems(data, context):
    await emit_event("state:entity:create", {...})
    await emit_event("monitor:agent_created", {...})
    await emit_event("metrics:agent_count", {...})
```

```yaml
# AFTER: Multi-target transformers (current approach)
transformers:
  - source: "agent:spawned"
    target: "state:entity:create"
    mapping: {...}
    
  - source: "agent:spawned"
    target: "monitor:agent_created"
    mapping: {...}
    
  - source: "agent:spawned"
    target: "metrics:agent_count"
    mapping: {...}
```

## Handler Analysis Tool

The `handler_analyzer.py` tool automatically analyzes Python files to identify migration candidates.

### Usage

```bash
# Analyze from KSI root directory
python var/lib/compositions/transformers/migration/migration_tools/handler_analyzer.py

# Analyze specific directory
python handler_analyzer.py /path/to/ksi
```

### Output

The tool generates a comprehensive `migration_analysis_report.json` with:
- Handler counts and distribution
- Pattern classification (simple_forwarder, field_mapper, etc.)
- Migration priority (high, medium, low, not_suitable)
- Code line counts and complexity scores
- Suggested migration phases

### Sample Analysis Output

```json
{
  "summary": {
    "total_handlers": 302,
    "suitable_for_migration": 201,
    "migration_percentage": 66.6
  },
  "pattern_distribution": {
    "simple_forwarder": 89,
    "field_mapper": 67,
    "conditional_router": 45,
    "multi_target": 34,
    "complex_logic": 67
  },
  "migration_phases": {
    "phase_1_easy_wins": {
      "count": 89,
      "estimated_code_reduction": 1245
    }
  }
}
```

## Validation Schemas

The `transformer_schemas.yaml` file contains JSON schemas for validating:
- Transformer structure and syntax
- Template variable correctness
- Condition expression validity
- Naming convention compliance

### Validation Example

```python
import jsonschema
import yaml

# Load schema
with open('validation/transformer_schemas.yaml') as f:
    schemas = yaml.safe_load(f)

# Validate transformer
transformer = {
    "source": "agent:spawned",
    "target": "monitor:agent_created", 
    "mapping": "{{$}}"
}

jsonschema.validate(transformer, schemas['schemas']['simple_forwarder'])
```

## Migration Workflow

### 1. Analysis Phase
```bash
# Run handler analysis
python migration_tools/handler_analyzer.py

# Review migration_analysis_report.json
# Identify high-priority candidates
```

### 2. Template Selection
- Review analysis report pattern classifications
- Choose appropriate template (simple_forwarder, field_mapper, etc.)
- Customize template for specific use case

### 3. Transformer Creation
- Copy relevant template
- Customize source/target events
- Update mapping configuration
- Add conditions if needed

### 4. Validation
- Validate against schema
- Test transformer behavior
- Verify integration tests pass

### 5. Handler Removal
- **BREAKING CHANGE**: Delete Python handler completely
- No backward compatibility or fallbacks
- Document breaking changes

## Migration Naming Conventions

### File Naming
- Service prefix: `agent_`, `orchestration_`, `monitor_`, etc.
- Pattern type: `forwarder`, `mapper`, `router`, `multi_target`
- Version: `v1`, `v2`, etc.
- Format: `{service}_{pattern}_{version}.yaml`

**Examples:**
- `agent_lifecycle_forwarder_v1.yaml`
- `completion_result_router_v1.yaml`
- `orchestration_status_mapper_v1.yaml`

### Transformer Naming
- Snake case, lowercase only
- Descriptive of functionality
- Include source and target context

**Examples:**
- `agent_spawned_to_monitor`
- `completion_error_to_alert`
- `orchestration_done_to_cleanup`

## Template Enhancement Features

### Enhanced Template Syntax
- `{{$}}` - Pass-through entire event data
- `{{var|default}}` - Default values for missing fields
- `{{_ksi_context.field}}` - Access system context
- `{{func()}}` - Function calls (timestamp_utc, len, upper, etc.)

### Available Functions
- `{{timestamp_utc()}}` - Current UTC timestamp
- `{{len(array)}}` - Array length
- `{{upper(text)}}` - Uppercase string
- `{{lower(text)}}` - Lowercase string
- `{{str(value)}}` - Convert to string
- `{{int(value)}}` - Convert to integer

### Context Access
- `{{_ksi_context._agent_id}}` - Current agent ID
- `{{_ksi_context._request_id}}` - Request ID
- `{{_ksi_context.orchestration_id}}` - Orchestration context

## Breaking Change Policy

**IMPORTANT**: This migration uses a breaking change approach:

1. **No Backward Compatibility**: Python handlers are deleted completely
2. **No Fallbacks**: No commented code or rollback mechanisms
3. **Complete Removal**: Legacy code is removed permanently
4. **Clean Architecture**: Move forward only, no hybrid systems

### Documentation Requirements
For each migration:
- Document original handler location
- List replaced functionality
- Note any behavior changes
- Record migration date and author

## Quality Assurance

### Pre-Migration Checklist
- [ ] Handler analysis completed
- [ ] Transformer template selected
- [ ] Mapping configuration validated
- [ ] Target events confirmed to exist
- [ ] Integration tests identified

### Post-Migration Checklist
- [ ] Transformer deployed and active
- [ ] Python handler deleted completely
- [ ] Integration tests pass
- [ ] Performance impact verified
- [ ] Breaking changes documented

## Support and Troubleshooting

### Common Issues

**Template Syntax Errors**
- Check `{{variable}}` syntax
- Verify field paths exist in source data
- Ensure function calls are supported

**Condition Evaluation**
- Use simple operators: `==`, `!=`, `>`, `<`
- Complex expressions not yet supported
- Field references must be valid

**Missing Target Events**
- Verify target event handlers exist
- Check event routing configuration
- Confirm service dependencies

### Getting Help

1. Review transformer templates for examples
2. Check validation schemas for syntax rules
3. Use handler analyzer for migration suggestions
4. Test transformers in development environment

---

## Migration Status

**Phase 1A Infrastructure**: ✅ COMPLETE
- Templates created for all pattern types
- Validation schemas implemented
- Handler analysis tool ready
- Documentation and examples provided

**Next Steps**: Phase 1B - Universal broadcast handler migration

This infrastructure supports the systematic migration of 200+ event handlers to declarative transformers, achieving 50-70% code reduction while maintaining system functionality.