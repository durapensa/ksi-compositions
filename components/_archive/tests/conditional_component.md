---
variables:
  environment:
    type: string
    default: production
    allowed_values: [development, staging, production]
  debug_mode:
    type: string
    default: false
conditions:
  - condition: environment == 'development'
    mixins:
      - test/phase3/debug_mixin
  - condition: environment == 'staging'
    mixins:
      - test/phase3/staging_mixin
---
# Conditional Component

This component demonstrates conditional mixin loading based on variables.

## Environment: {{environment}}

Environment-specific content will be loaded based on the environment variable.

## Base Configuration
This content always appears regardless of environment.