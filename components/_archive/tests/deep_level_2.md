---
extends: test/phase3/deep_level_1
variables:
  level:
    type: string
    default: "2"
---
# Deep Level 2

This is level {{level}} extending from level 1.

## Level 2 Additional Content
- Extended functionality
- Additional features
- Performance optimizations