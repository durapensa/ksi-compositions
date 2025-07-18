---
extends: test/phase3/deep_level_2
mixins:
  - test/phase3/greeting_mixin
variables:
  level:
    type: string
    default: "3"
  name:
    type: string
    default: "Deep Test User"
---
# Deep Level 3

This is level {{level}} with multiple inheritance layers and mixins.

## Level 3 Advanced Content
- Multi-level inheritance
- Mixin integration
- Complex variable resolution