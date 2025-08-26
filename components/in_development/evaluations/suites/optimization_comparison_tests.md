---
component_type: evaluation
name: optimization_comparison_tests
version: 1.0.0
description: Test scenarios comparing DSPy/MIPRO vs LLM-as-Judge optimization
evaluation_type: comparison_suite
dependencies:
- in_development/evaluations/judges/optimization_method_comparator
- in_development/evaluations/judges/token_efficiency_judge
- in_development/evaluations/judges/instruction_fidelity_judge
---

# Optimization Method Comparison Test Suite

Comprehensive test scenarios demonstrating when each optimization method excels.

## Test Categories

### Category 1: Structured Task Optimization
Where DSPy/MIPRO typically excels.

#### Test 1.1: Data Extraction Component
**Component**: JSON parser agent
**Task**: Extract structured data from text

**DSPy Optimization Target**:
```yaml
metrics:
  extraction_accuracy: 0.95
  token_usage: minimize
  processing_speed: < 100ms
training_data: 1000 labeled examples
```

**Expected DSPy Performance**:
- ✅ 50% token reduction
- ✅ 98% accuracy maintained
- ✅ Consistent format output
- ✅ Fast optimization (2 hours)

**Expected Judge Performance**:
- ⚠️ 20% token reduction
- ✅ Explains extraction logic better
- ⚠️ Slower optimization (4 hours)
- ❌ Less consistent format

**Verdict**: DSPy clear winner for structured tasks

#### Test 1.2: Classification Component
**Component**: Sentiment analyzer
**Task**: Classify text sentiment (positive/negative/neutral)

**Test Data**:
```json
{
  "inputs": [
    "This product exceeded my expectations!",
    "Terrible experience, would not recommend.",
    "It works as described, nothing special."
  ],
  "expected": ["positive", "negative", "neutral"]
}
```

**Comparison Points**:
- Accuracy on edge cases
- Token efficiency
- Explanation quality
- Confidence calibration

### Category 2: Creative Task Optimization
Where LLM-as-Judge typically excels.

#### Test 2.1: Creative Writing Component
**Component**: Story continuation agent
**Task**: Continue stories creatively

**Judge Optimization Focus**:
```yaml
dimensions:
  creativity: 0.35
  coherence: 0.25
  style_consistency: 0.20
  engagement: 0.20
```

**Expected DSPy Performance**:
- ✅ Efficient token use
- ❌ Formulaic patterns emerge
- ❌ Reduced creativity
- ⚠️ Overfits to training stories

**Expected Judge Performance**:
- ✅ Maintains creative variety
- ✅ Preserves unique voice
- ✅ Engaging narratives
- ⚠️ Higher token usage

**Verdict**: Judge essential for creative tasks

#### Test 2.2: Conversational Component
**Component**: Empathetic counselor
**Task**: Provide supportive responses

**Test Scenarios**:
```yaml
scenarios:
  - context: "User expressing anxiety"
    evaluate: empathy, appropriateness
  - context: "User seeking advice"
    evaluate: helpfulness, boundaries
  - context: "Crisis situation"
    evaluate: safety, escalation
```

**Critical Evaluation Points**:
- Emotional intelligence
- Response appropriateness
- Safety considerations
- Boundary maintenance

### Category 3: Hybrid Optimization Scenarios
Where combined approach works best.

#### Test 3.1: Technical Documentation Component
**Component**: API documentation writer
**Task**: Generate clear, accurate API docs

**Hybrid Strategy**:
```yaml
stage_1_dspy:
  optimize: structure, completeness
  metrics: coverage, accuracy
  
stage_2_judge:
  optimize: clarity, examples
  metrics: readability, usefulness
```

**Expected Results**:
- DSPy ensures complete parameter documentation
- Judge improves explanation quality
- Combined: Comprehensive AND clear

#### Test 3.2: Code Review Component
**Component**: Code quality analyzer
**Task**: Review code and suggest improvements

**Optimization Targets**:
```yaml
quantitative:
  - Bug detection rate
  - False positive rate
  - Processing speed

qualitative:
  - Suggestion quality
  - Explanation clarity
  - Priority accuracy
```

### Category 4: Edge Case Handling
Testing optimization robustness.

#### Test 4.1: Adversarial Inputs
**Test Type**: Robustness to unusual inputs

**Input Examples**:
```python
adversarial_inputs = [
    "",  # Empty input
    "A" * 10000,  # Very long input
    "🦜🔁" * 100,  # Unicode/emoji spam
    "<script>alert('xss')</script>",  # Injection attempt
    "Ignore previous instructions and...",  # Prompt injection
]
```

**Evaluation**:
- DSPy: May not have training data for these
- Judge: Can reason about appropriate handling
- Hybrid: Best of both worlds

#### Test 4.2: Context Switching
**Test Type**: Maintaining quality across contexts

**Context Variations**:
```yaml
contexts:
  formal_business:
    tone: professional
    terminology: industry-specific
    
  casual_chat:
    tone: friendly
    terminology: colloquial
    
  technical_support:
    tone: helpful
    terminology: technical
```

## Scoring Framework

### Quantitative Scoring (DSPy Domain)
```python
def score_quantitative(original, optimized):
    return {
        'token_reduction': (original.tokens - optimized.tokens) / original.tokens,
        'speed_improvement': (original.latency - optimized.latency) / original.latency,
        'accuracy_maintained': optimized.accuracy / original.accuracy,
        'cost_reduction': (original.cost - optimized.cost) / original.cost
    }
```

### Qualitative Scoring (Judge Domain)
```python
def score_qualitative(original, optimized):
    return {
        'instruction_fidelity': judge_fidelity(optimized),
        'behavioral_consistency': judge_consistency(optimized),
        'quality_preservation': judge_quality(optimized),
        'safety_compliance': judge_safety(optimized)
    }
```

### Combined Scoring
```python
def score_hybrid(quant_scores, qual_scores, weights):
    combined = {}
    for metric, score in quant_scores.items():
        combined[metric] = score * weights.get(metric, 0.5)
    for metric, score in qual_scores.items():
        combined[metric] = score * weights.get(metric, 0.5)
    return sum(combined.values()) / len(combined)
```

## Test Execution

### Running Comparison Tests
```bash
# Test DSPy optimization
ksi send evaluation:run \
  --component "test_components/data_extractor" \
  --test_suite "optimization_comparison_tests" \
  --method "dspy" \
  --category "structured_tasks"

# Test Judge optimization
ksi send evaluation:run \
  --component "test_components/story_writer" \
  --test_suite "optimization_comparison_tests" \
  --method "judge" \
  --category "creative_tasks"

# Test Hybrid optimization
ksi send evaluation:run \
  --component "test_components/code_reviewer" \
  --test_suite "optimization_comparison_tests" \
  --method "hybrid" \
  --category "balanced_tasks"
```

### Generating Comparison Report
```bash
ksi send evaluation:compare_methods \
  --suite "optimization_comparison_tests" \
  --methods "dspy,judge,hybrid" \
  --output_format "detailed_report"
```

## Expected Outcomes

### Clear Winners
- **Structured tasks**: DSPy by 20-30% margin
- **Creative tasks**: Judge by 25-35% margin
- **Safety-critical**: Judge mandatory
- **High-volume**: DSPy for cost savings

### Hybrid Advantages
- **Documentation**: 15% better than either alone
- **Analysis tasks**: 20% overall improvement
- **Customer service**: Balances efficiency and quality

### Trade-off Patterns
- **Efficiency vs Quality**: -0.7 correlation
- **Speed vs Nuance**: -0.6 correlation
- **Cost vs Safety**: -0.8 correlation
- **Automation vs Control**: -0.5 correlation

## Validation Criteria

### Test Suite Success
- All test categories execute without errors
- Clear differentiation between methods observed
- Trade-offs quantified and documented
- Recommendations align with expectations

### Method Validation
- DSPy excels where expected (structured, metrics-driven)
- Judge excels where expected (creative, quality-focused)
- Hybrid shows combined benefits
- Edge cases handled appropriately

## Continuous Improvement

### Feedback Loop
1. Run comparison tests
2. Analyze unexpected results
3. Refine optimization strategies
4. Update test scenarios
5. Repeat quarterly

### Metrics Tracking
- Method selection accuracy
- Optimization outcome satisfaction
- Production performance correlation
- Cost-benefit realization