#!/bin/bash
# Fix mixin references in components

echo "Fixing mixin references..."
echo "========================="

cd /Users/dp/projects/ksi/var/lib/compositions/components_new

# Function to fix mixins in a file
fix_file() {
    local file="$1"
    local changed=0
    
    echo "Checking: $file"
    
    # Create temp file
    cp "$file" /tmp/mixin_temp.txt
    
    # Apply replacements
    if grep -q "components/agent_instructions/" /tmp/mixin_temp.txt; then
        sed -i '' "s|components/agent_instructions/|behaviors/communication/|g" /tmp/mixin_temp.txt
        echo "  ✓ Updated agent_instructions path"
        changed=1
    fi
    
    if grep -q "components/capabilities/claude_code_1.0.x/" /tmp/mixin_temp.txt; then
        sed -i '' "s|components/capabilities/claude_code_1.0.x/|behaviors/communication/|g" /tmp/mixin_temp.txt
        echo "  ✓ Updated claude_code capabilities path"
        changed=1
    fi
    
    if grep -q "capabilities/claude_code_1.0.x/" /tmp/mixin_temp.txt; then
        sed -i '' "s|capabilities/claude_code_1.0.x/|behaviors/communication/|g" /tmp/mixin_temp.txt
        echo "  ✓ Updated capabilities path"
        changed=1
    fi
    
    if grep -q "components/base/" /tmp/mixin_temp.txt; then
        sed -i '' "s|components/base/|core/|g" /tmp/mixin_temp.txt
        echo "  ✓ Updated base component path"
        changed=1
    fi
    
    if grep -q "components/personas/" /tmp/mixin_temp.txt; then
        sed -i '' "s|components/personas/|personas/|g" /tmp/mixin_temp.txt
        echo "  ✓ Updated personas path"
        changed=1
    fi
    
    if grep -q "components/agents/" /tmp/mixin_temp.txt; then
        sed -i '' "s|components/agents/|personas/analysts/|g" /tmp/mixin_temp.txt
        echo "  ✓ Updated agents path"
        changed=1
    fi
    
    # Update file if changed
    if [ $changed -eq 1 ]; then
        mv /tmp/mixin_temp.txt "$file"
    else
        echo "  - No mixin changes needed"
        rm /tmp/mixin_temp.txt
    fi
}

# Fix all markdown files
find . -name "*.md" -type f ! -path "./_archive/*" | while read file; do
    fix_file "$file"
done

# Check for any yaml/profile references we need to update
echo -e "\nChecking for profile references to update..."
if [ -d ../profiles ]; then
    # Just check base_single_agent as a key file
    if [ -f ../profiles/base/base_single_agent.yaml ]; then
        echo "Found profiles that may need updating"
        # Show what needs fixing
        grep -l "components/" ../profiles/**/*.yaml 2>/dev/null | head -5
    fi
fi

echo -e "\nMixin reference update complete!"