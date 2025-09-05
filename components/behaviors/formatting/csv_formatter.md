---
component_type: behavior
name: csv_formatter
version: 1.0.0
description: Provides CSV formatting capabilities for data extraction
---

# CSV Formatter Behavior

You have the capability to format data as CSV (Comma-Separated Values).

## CSV Formatting Rules

When formatting data as CSV:
1. First row contains column headers
2. Each subsequent row is a data record
3. Handle nested objects by flattening or JSON-encoding them
4. Escape commas and quotes properly
5. Use consistent field ordering

## Field Selection

When selecting fields for CSV output:
- Include entity_id and created_at by default
- Extract specified fields from properties
- Handle missing fields with empty values
- Preserve data types where possible

## Example CSV Output

```csv
entity_id,created_at,communication_level,cooperation_rate
exp_001,1757079759.73,0.15,0.3
exp_002,1757079794.99,0.225,0.7
exp_003,1757079838.27,0.1875,0.55
```

## Handling Complex Data

For nested structures in CSV:
- Simple values: Direct inclusion
- Arrays: JSON-encode as string
- Objects: JSON-encode or flatten with dot notation
- Nulls: Empty string

You understand CSV formatting best practices for data analysis tools.