---
extends: components/base.md
mixins:
  - components/missing_quotes: invalid_value
  - components/bad_indentation
    extra_indented: true
variables:
  unclosed_list: [
    item1,
    item2
  missing_bracket: true
  invalid_syntax: "unclosed string
---
# Malformed YAML Test

This component has intentionally malformed YAML frontmatter to test error handling in the Progressive Component System.