---
component_type: evaluation
name: component_improvement
version: 1.0.0
description: Test suite for evaluating agent ability to improve components
test_scenarios:
  - analyze_component
  - identify_improvements
  - create_improved_version
  - quantify_improvements
success_criteria:
  - valid_analysis: 100%
  - specific_recommendations: 90%
  - improved_version_created: 100%
  - measurable_improvement: 80%
---

# Component Improvement Evaluation Suite

## Overview

Evaluates whether an agent can successfully analyze, improve, and create better versions of existing components.

## Test Scenarios

### Scenario 1: Simple Component Analysis

#### Input Component
```yaml
---
component_type: agent
name: basic_greeter
---
You are a greeting agent. When someone says hello, respond with "Greetings!"
```

#### Test 1.1: Component Analysis
**Prompt**: "Analyze this component and identify areas for improvement"
**Expected**: Specific analysis identifying:
- Token inefficiency
- Limited greeting variety
- No personalization
**Success Criteria**: At least 3 specific improvement areas identified

#### Test 1.2: Improvement Recommendations
**Prompt**: "Provide specific recommendations to improve this component"
**Expected**: Actionable recommendations like:
- "Reduce instructions to essential behavior"
- "Add context awareness"
- "Support multiple greeting styles"
**Success Criteria**: Concrete, implementable suggestions

### Scenario 2: Component Optimization

#### Test 2.1: Token Reduction
**Prompt**: "Create an improved version that uses 50% fewer tokens"
**Expected**: Functionally equivalent component with reduced size
**Success**: New component maintains behavior with fewer tokens
**Measurement**: Token count comparison

#### Test 2.2: Feature Enhancement
**Prompt**: "Add time-of-day awareness to the greeting"
**Expected**: Component that greets differently based on time
**Success**: Enhanced functionality demonstrated
**Validation**: Test with different times

### Scenario 3: Complex Component Improvement

#### Input Component
```yaml
---
component_type: persona
name: data_analyst
dependencies:
  - core/base_agent
---
You are a Senior Data Analyst with 15 years of experience in statistical analysis, machine learning, and data visualization. You excel at finding patterns in complex datasets and communicating insights clearly to both technical and non-technical audiences. You have expertise in Python, R, SQL, and various BI tools.
```

#### Test 3.1: Structural Improvement
**Prompt**: "Improve the structure and organization of this component"
**Expected**: Better organized component with:
- Clear capability sections
- Separated skills and tools
- Improved readability
**Success**: Demonstrable structural improvements

#### Test 3.2: Behavioral Enhancement  
**Prompt**: "Enhance this component to be more action-oriented"
**Expected**: Component focused on doing rather than describing
**Success**: Behavioral shift evident in improved version

### Scenario 4: Quantitative Improvement

#### Test 4.1: Measurable Metrics
**Prompt**: "Improve this component and quantify the improvements"
**Expected**: Agent provides metrics like:
- Token reduction: 35%
- Clarity score: +20%
- Action orientation: +40%
**Success**: Specific, measurable improvements cited

#### Test 4.2: Validation Plan
**Prompt**: "How would you validate the improvements?"
**Expected**: Concrete validation approach:
- Test cases to run
- Metrics to measure
- Comparison methodology
**Success**: Actionable validation plan provided

## Scoring Framework

### Analysis Quality (25%)
- Identifies multiple improvement areas
- Provides specific, not generic feedback
- Demonstrates understanding of component purpose

### Recommendation Specificity (25%)
- Actionable suggestions
- Clear implementation path
- Addresses identified issues

### Implementation Success (25%)
- Creates valid improved component
- Maintains original functionality
- Achieves stated improvements

### Quantification (25%)
- Provides measurable metrics
- Accurate improvement calculations
- Offers validation approach

## Test Protocol

1. **Component Selection**
   - Use test components of varying complexity
   - Include different component types
   - Test edge cases

2. **Agent Testing**
   - Spawn agent with improvement capabilities
   - Provide component and improvement goal
   - Capture all outputs

3. **Validation**
   - Verify improved component syntax
   - Test functionality preservation
   - Measure actual improvements

4. **Scoring**
   - Score each criterion
   - Calculate weighted total
   - Document specific successes/failures

## Usage Example

```bash
# Test a component improvement agent
ksi send evaluation:run \
  --component_path "agents/component_improver" \
  --test_suite "component_improvement" \
  --model "claude-sonnet-4-20250514" \
  --vars '{"test_component": "personas/basic_greeter"}'
```

## Success Metrics

- **Pass**: Total score >= 85% 
- **Conditional Pass**: 70-84% (specific improvements needed)
- **Fail**: < 70%

## Integration

- Results stored in unified index
- Can chain with optimization tools
- Feeds into larger optimization orchestrations