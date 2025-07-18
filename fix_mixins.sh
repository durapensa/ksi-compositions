#!/bin/bash
# Fix mixin references in components

echo "Fixing mixin references..."
echo "========================="

cd /Users/dp/projects/ksi/var/lib/compositions/components_new

# Define path replacements
declare -A replacements=(
    ["components/agent_instructions/"]="behaviors/communication/"
    ["components/capabilities/claude_code_1.0.x/"]="behaviors/communication/"
    ["components/capabilities/"]="behaviors/"
    ["components/base/"]="core/"
    ["components/personas/"]="personas/"
    ["components/agents/"]="personas/analysts/"
    ["capabilities/claude_code_1.0.x/"]="behaviors/communication/"
    ["components/evaluations/"]="evaluations/quality/"
)

# Function to fix mixins in a file
fix_file() {
    local file="$1"
    local changed=0
    
    echo "Checking: $file"
    
    # Create temp file
    cp "$file" /tmp/mixin_temp.txt
    
    # Apply replacements
    for old in "${!replacements[@]}"; do
        new="${replacements[$old]}"
        if grep -q "$old" /tmp/mixin_temp.txt; then
            sed -i '' "s|$old|$new|g" /tmp/mixin_temp.txt
            echo "  ✓ Replaced: $old → $new"
            changed=1
        fi
    done
    
    # Update file if changed
    if [ $changed -eq 1 ]; then
        mv /tmp/mixin_temp.txt "$file"
    else
        echo "  - No mixin changes needed"
    fi
}

# Fix all markdown files
find . -name "*.md" -type f ! -path "./_archive/*" | while read file; do
    fix_file "$file"
done

# Also fix the few remaining yaml files in profiles
if [ -d ../profiles ]; then
    echo -e "\nFixing profile references..."
    find ../profiles -name "*.yaml" -type f | while read file; do
        # Only process if it contains mixin references
        if grep -q "mixins:" "$file" || grep -q "components/" "$file"; then
            fix_file "$file"
        fi
    done
fi

echo -e "\nMixin reference update complete!"