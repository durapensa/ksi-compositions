---
component_type: optimization
name: text_analysis_signature
version: 1.0.0
description: DSPy signature for text analysis with insights and recommendations
author: claude_code
capabilities:
  - dspy_signature
  - text_analysis
  - optimization_target
---

# Text Analysis DSPy Signature

This component defines a DSPy signature for text analysis optimization.

## DSPy Signature Definition

```python
import dspy

class TextAnalysisSignature(dspy.Signature):
    """Analyze text and provide insights with actionable recommendations."""
    
    # Input fields
    text: str = dspy.InputField(desc="Text to analyze")
    domain: str = dspy.InputField(desc="Domain context (business, technical, academic)")
    
    # Output fields  
    insights: str = dspy.OutputField(desc="Key insights from the text analysis")
    recommendations: str = dspy.OutputField(desc="Specific actionable recommendations")
    confidence: float = dspy.OutputField(desc="Confidence score 0.0-1.0")

# Usage example for optimization
signature = TextAnalysisSignature()
```

## Optimization Parameters

- **Input Variability**: text (any content), domain (3 categories)
- **Output Quality Metrics**: insight depth, recommendation specificity, confidence calibration
- **Training Data Requirements**: 20+ examples per domain
- **Evaluation Criteria**: Multi-factor scoring (content quality + confidence accuracy)

## Integration Points

- Use with MIPRO for automated parameter tuning
- Compatible with judge-based evaluation frameworks
- Supports hybrid optimization pipelines