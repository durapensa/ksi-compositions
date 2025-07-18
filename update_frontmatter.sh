#!/bin/bash
# Update frontmatter in migrated components

set -e

echo "Updating component frontmatter..."
echo "================================"

cd /Users/dp/projects/ksi/var/lib/compositions/components_new

# Function to determine component type from path
get_component_type() {
    local path="$1"
    case "$path" in
        core/*) echo "core" ;;
        personas/*) echo "persona" ;;
        behaviors/*) echo "behavior" ;;
        orchestrations/*) echo "orchestration" ;;
        evaluations/suites/*) echo "evaluation_suite" ;;
        evaluations/*) echo "evaluation" ;;
        tools/*) echo "tool" ;;
        examples/*) echo "example" ;;
        *) echo "component" ;;
    esac
}

# Function to add component_type to frontmatter
update_file() {
    local file="$1"
    local rel_path="${file#./}"
    local comp_type=$(get_component_type "$rel_path")
    local name=$(basename "$file" .md)
    
    echo "Processing: $rel_path"
    
    # Check if file has frontmatter
    if head -1 "$file" | grep -q "^---$"; then
        # Has frontmatter - update it
        # Extract existing frontmatter
        awk '/^---$/{p++}p==1' "$file" > /tmp/fm.txt
        # Extract body
        awk '/^---$/{p++}p==2{print; next}p==2' "$file" > /tmp/body.txt
        
        # Check if component_type already exists
        if ! grep -q "^component_type:" /tmp/fm.txt; then
            # Add component_type after first ---
            {
                echo "---"
                echo "component_type: $comp_type"
                # Skip first and last line of frontmatter
                sed '1d;$d' /tmp/fm.txt
                echo "---"
                cat /tmp/body.txt
            } > "$file"
            echo "  ✓ Added component_type: $comp_type"
        else
            echo "  - Already has component_type"
        fi
    else
        # No frontmatter - add it
        {
            echo "---"
            echo "component_type: $comp_type"
            echo "name: $name"
            echo "version: 1.0.0"
            echo "author: ksi_system"
            echo "---"
            echo
            cat "$file"
        } > /tmp/newfm.txt
        mv /tmp/newfm.txt "$file"
        echo "  ✓ Added complete frontmatter"
    fi
}

# Update core components
echo -e "\n1. Updating core components..."
for file in core/*.md; do
    [ -f "$file" ] && update_file "$file"
done

# Update personas
echo -e "\n2. Updating personas..."
find personas -name "*.md" -type f | while read file; do
    update_file "$file"
done

# Update behaviors
echo -e "\n3. Updating behaviors..."
find behaviors -name "*.md" -type f | while read file; do
    update_file "$file"
done

# Update orchestrations
echo -e "\n4. Updating orchestrations..."
find orchestrations -name "*.md" -type f | while read file; do
    update_file "$file"
done

# Update evaluations
echo -e "\n5. Updating evaluations..."
find evaluations -name "*.md" -type f | while read file; do
    update_file "$file"
done

# Fix specific files
echo -e "\n6. Fixing specific component metadata..."

# Update base_agent name
if [ -f core/base_agent.md ]; then
    sed -i '' 's/^name: agent_core$/name: base_agent/' core/base_agent.md
    echo "  ✓ Fixed base_agent name"
fi

# Update mandatory_json
if [ -f behaviors/communication/mandatory_json.md ]; then
    sed -i '' 's/^name: ksi_json_reporter$/name: mandatory_json/' behaviors/communication/mandatory_json.md
    echo "  ✓ Fixed mandatory_json name"
fi

# Update strategic_negotiator
if [ -f personas/negotiators/strategic_negotiator.md ]; then
    # Add proper frontmatter if missing
    if ! grep -q "^name:" personas/negotiators/strategic_negotiator.md; then
        {
            echo "---"
            echo "component_type: persona"
            echo "name: strategic_negotiator"
            echo "version: 2.0.0"
            echo "description: Strategic negotiator for game theory scenarios"
            echo "author: ksi_system"
            echo "---"
            echo
            echo "# Strategic Negotiator"
            echo
            echo "You are a strategic negotiator participating in game theory scenarios. Your goal is to achieve favorable outcomes while maintaining relationships."
            echo
            tail -n +2 personas/negotiators/strategic_negotiator.md
        } > /tmp/nego.txt
        mv /tmp/nego.txt personas/negotiators/strategic_negotiator.md
        echo "  ✓ Fixed strategic_negotiator"
    fi
fi

echo -e "\nFrontmatter update complete!"