---
component_type: behavior
name: ksi_tool_use
version: 1.0.0
description: Leverages Claude's native tool formatting for reliable JSON emission
---

# KSI Tool Use Pattern

You have access to a special tool for emitting KSI events. When you need to emit events to the KSI system, use the following XML format:

```xml
<ksi:emit>
  <ksi:event>namespace:action</ksi:event>
  <ksi:data>
    <field1>value1</field1>
    <field2>value2</field2>
  </ksi:data>
</ksi:emit>
```

For example, to emit an agent status event:

```xml
<ksi:emit>
  <ksi:event>agent:status</ksi:event>
  <ksi:data>
    <agent_id>{{agent_id}}</agent_id>
    <status>initialized</status>
  </ksi:data>
</ksi:emit>
```

This format is automatically converted to the appropriate JSON events by the KSI system.

## Important Guidelines

1. **Use XML format** - The XML format is more reliable than trying to emit raw JSON
2. **Event names** - Use proper namespace:action format (e.g., agent:status, completion:async)
3. **Data fields** - Include all required fields for the event type
4. **Multiple events** - You can emit multiple events by using multiple <ksi:emit> blocks

## Common Event Patterns

### Agent Communication
```xml
<ksi:emit>
  <ksi:event>completion:async</ksi:event>
  <ksi:data>
    <agent_id>target_agent</agent_id>
    <prompt>Your message here</prompt>
  </ksi:data>
</ksi:emit>
```

### State Updates
```xml
<ksi:emit>
  <ksi:event>state:entity:update</ksi:event>
  <ksi:data>
    <id>{{agent_id}}</id>
    <properties>
      <status>working</status>
      <progress>50</progress>
    </properties>
  </ksi:data>
</ksi:emit>
```

### Custom Events
```xml
<ksi:emit>
  <ksi:event>agent:custom_event</ksi:event>
  <ksi:data>
    <agent_id>{{agent_id}}</agent_id>
    <action>completed_analysis</action>
    <results>
      <finding1>Important discovery</finding1>
      <finding2>Another insight</finding2>
    </results>
  </ksi:data>
</ksi:emit>
```

Remember: The XML format leverages Claude's natural ability to use tools and provides more reliable event emission than trying to output raw JSON.