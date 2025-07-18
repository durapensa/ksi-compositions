#\!/usr/bin/env python3
import json
import socket
import time

# Create test component with agent_id template
component_content = """# Test Agent ID Substitution

## MANDATORY: Start your response with this exact JSON:
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "initialized", "task": "test"}}

You are agent {{agent_id}} testing variable substitution.

End with:
{"event": "agent:status", "data": {"agent_id": "{{agent_id}}", "status": "completed", "task": "test", "result": "success"}}"""

# Create component
create_event = {
    "event": "composition:create_component",
    "data": {
        "name": "components/test/agent_id_substitution",
        "content": component_content,
        "description": "Test agent_id substitution"
    }
}

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('var/run/daemon.sock')
sock.send(json.dumps(create_event).encode() + b'\n')
response = json.loads(sock.recv(65536).decode())
print(f"Created component: {response['data']['status']}")
sock.close()

# Spawn agent
spawn_event = {
    "event": "agent:spawn_from_component",
    "data": {
        "component": "components/test/agent_id_substitution",
        "prompt": "Test the variable substitution system."
    }
}

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('var/run/daemon.sock')
sock.send(json.dumps(spawn_event).encode() + b'\n')
response = json.loads(sock.recv(65536).decode())
agent_id = response['data'].get('agent_id')
print(f"Spawned agent: {agent_id}")
sock.close()

print("\nWaiting 30 seconds for processing...")
time.sleep(30)

# Check for events
monitor_event = {
    "event": "monitor:get_events",
    "data": {
        "event_patterns": ["agent:status"],
        "limit": 10
    }
}

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('var/run/daemon.sock')
sock.send(json.dumps(monitor_event).encode() + b'\n')
response = json.loads(sock.recv(65536).decode())
sock.close()

# Find events from our agent
agent_events = []
for event in response['data']['events']:
    if event.get('data', {}).get('agent_id') == agent_id:
        agent_events.append(event)
        print(f"\nFound event: {event['event_name']}")
        print(f"  agent_id: {event['data']['agent_id']}")
        print(f"  status: {event['data'].get('status')}")

if not agent_events:
    print(f"\nNo events found for {agent_id}")
else:
    print(f"\n✓ Successfully found {len(agent_events)} events with correct agent_id\!")
