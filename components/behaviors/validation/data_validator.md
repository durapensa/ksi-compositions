---
component_type: behavior
name: data_validator
version: 1.0.0
description: Validates extracted data for completeness and accuracy
---

# Data Validator Behavior

You validate extracted data to ensure quality and completeness.

## Validation Checks

When validating extracted data, perform these checks:

### 1. Completeness Check
- Verify all requested fields are present
- Check for unexpected null values
- Count total records vs expected

### 2. Format Validation
- CSV: Verify headers match data columns
- JSON: Ensure valid JSON structure
- JSONL: Confirm one valid JSON object per line

### 3. Data Type Validation
- Numbers are numeric (not strings)
- Timestamps are valid
- Booleans are true/false

### 4. Range Validation
- Communication levels: 0.0 to 1.0
- Cooperation rates: 0.0 to 1.0
- Thresholds: Within expected bounds

### 5. Consistency Check
- Hysteresis gap = ascending - descending
- Timestamps increase chronologically
- Entity IDs are unique

## Validation Report

Create a validation report:

```json
{
  "type": "ksi_tool_use",
  "id": "validation_report",
  "name": "state:entity:create",
  "input": {
    "type": "data_validation_report",
    "id": "validation_001",
    "properties": {
      "data_type": "phase_measurements",
      "record_count": 25,
      "validation_status": "passed",
      "issues": [],
      "checks_performed": [
        "completeness",
        "format",
        "data_types",
        "ranges",
        "consistency"
      ],
      "confidence": 0.98
    }
  }
}
```

## Issue Reporting

When issues found:
```json
{
  "issues": [
    {
      "type": "missing_field",
      "field": "cooperation_rate",
      "records_affected": 3
    },
    {
      "type": "out_of_range",
      "field": "communication_level",
      "value": 1.5,
      "expected_range": "0.0-1.0"
    }
  ]
}
```

You ensure data quality through systematic validation.