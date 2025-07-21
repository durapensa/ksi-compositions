---
component_type: evaluation
name: llm_judge_evaluator
version: 1.0.0
description: LLM-as-Judge evaluation for text analysis optimization
author: claude_code
capabilities:
  - llm_judge
  - qualitative_evaluation
  - optimization_metrics
dependencies:
  - components/optimization/signatures/text_analysis_signature
---

# LLM Judge Text Analysis Evaluator

This component implements LLM-as-Judge evaluation for the TextAnalysisSignature optimization.

## Judge Evaluation Implementation

```python
import dspy
from typing import Dict, Any, List
import json

class LLMJudgeEvaluator:
    """LLM-as-Judge evaluator for text analysis quality"""
    
    def __init__(self, judge_model: str = "claude-cli/sonnet"):
        self.judge_model = judge_model
        self.judge_signature = JudgeSignature()
        self.judge_module = dspy.Predict(self.judge_signature)
    
    def evaluate_example(self, prediction, ground_truth, trace=None) -> float:
        """Evaluate prediction using LLM judge"""
        
        # Prepare judge input
        evaluation_context = self._prepare_judge_context(prediction, ground_truth)
        
        # Get judge assessment
        with dspy.context(lm=dspy.LM(self.judge_model)):
            judge_result = self.judge_module(
                original_text=ground_truth.get('text', ''),
                domain=ground_truth.get('domain', ''),
                insights=prediction.insights,
                recommendations=prediction.recommendations,
                confidence=str(prediction.confidence),
                evaluation_criteria=evaluation_context
            )
        
        # Parse judge score
        try:
            score_data = json.loads(judge_result.score_breakdown)
            final_score = score_data.get('overall_score', 0.0)
            return min(1.0, max(0.0, final_score))
        except:
            # Fallback parsing if JSON fails
            return self._parse_fallback_score(judge_result.overall_assessment)
    
    def _prepare_judge_context(self, prediction, ground_truth) -> str:
        """Prepare evaluation criteria for the judge"""
        return """
        Evaluate the text analysis on these criteria:
        
        1. INSIGHT QUALITY (0.0-1.0):
           - Depth of analysis beyond surface-level observations
           - Relevance to the domain context
           - Novel perspectives or connections identified
        
        2. RECOMMENDATION PRACTICALITY (0.0-1.0):
           - Specificity and actionability of suggestions
           - Feasibility within the domain context
           - Clear implementation guidance
        
        3. CONFIDENCE CALIBRATION (0.0-1.0):
           - Accuracy of confidence score relative to actual quality
           - Appropriate uncertainty for complex/ambiguous content
           - Consistent with depth of analysis provided
        
        Return scores as JSON: {"insight_quality": X.X, "recommendation_practicality": X.X, "confidence_calibration": X.X, "overall_score": X.X}
        """
    
    def _parse_fallback_score(self, assessment_text: str) -> float:
        """Fallback score parsing if JSON fails"""
        # Look for explicit scores in text
        import re
        scores = re.findall(r'(\d+\.?\d*)\s*/\s*1\.?0?', assessment_text)
        if scores:
            return float(scores[0])
        
        # Sentiment-based scoring
        positive_words = ['excellent', 'good', 'strong', 'clear', 'effective']
        negative_words = ['poor', 'weak', 'unclear', 'ineffective', 'lacking']
        
        pos_count = sum(1 for word in positive_words if word in assessment_text.lower())
        neg_count = sum(1 for word in negative_words if word in assessment_text.lower())
        
        if pos_count > neg_count:
            return 0.7
        elif neg_count > pos_count:
            return 0.3
        else:
            return 0.5

class JudgeSignature(dspy.Signature):
    """Signature for LLM judge evaluation"""
    
    original_text: str = dspy.InputField(desc="Original text that was analyzed")
    domain: str = dspy.InputField(desc="Domain context (business, technical, academic)")
    insights: str = dspy.InputField(desc="Generated insights to evaluate")
    recommendations: str = dspy.InputField(desc="Generated recommendations to evaluate")
    confidence: str = dspy.InputField(desc="Confidence score from the model")
    evaluation_criteria: str = dspy.InputField(desc="Detailed evaluation criteria")
    
    score_breakdown: str = dspy.OutputField(desc="JSON with individual criterion scores")
    overall_assessment: str = dspy.OutputField(desc="Detailed qualitative assessment")
    strengths: str = dspy.OutputField(desc="Key strengths identified")
    weaknesses: str = dspy.OutputField(desc="Areas for improvement")

# Usage with optimization pipeline
def create_judge_evaluator():
    evaluator = LLMJudgeEvaluator()
    return evaluator.evaluate_example
```

## Judge Prompt Engineering

```python
class EnhancedJudgeModule(dspy.Module):
    """Enhanced judge with domain-specific expertise"""
    
    def __init__(self):
        super().__init__()
        self.domain_experts = {
            'business': BusinessExpertJudge(),
            'technical': TechnicalExpertJudge(), 
            'academic': AcademicExpertJudge()
        }
    
    def forward(self, prediction, ground_truth):
        domain = ground_truth.get('domain', 'business')
        expert_judge = self.domain_experts.get(domain, self.domain_experts['business'])
        
        return expert_judge(
            text=ground_truth.get('text'),
            insights=prediction.insights,
            recommendations=prediction.recommendations,
            confidence=prediction.confidence
        )

class BusinessExpertJudge(dspy.Signature):
    """Business domain expert judge"""
    text: str = dspy.InputField()
    insights: str = dspy.InputField()
    recommendations: str = dspy.InputField() 
    confidence: float = dspy.InputField()
    
    business_score: float = dspy.OutputField(desc="Score for business relevance and ROI focus")
    strategic_value: str = dspy.OutputField(desc="Assessment of strategic business value")
    implementation_feasibility: str = dspy.OutputField(desc="Feasibility within business context")

class TechnicalExpertJudge(dspy.Signature):
    """Technical domain expert judge"""
    text: str = dspy.InputField()
    insights: str = dspy.InputField()
    recommendations: str = dspy.InputField()
    confidence: float = dspy.InputField()
    
    technical_accuracy: float = dspy.OutputField(desc="Technical accuracy and depth")
    scalability_assessment: str = dspy.OutputField(desc="Scalability and architecture considerations")
    implementation_complexity: str = dspy.OutputField(desc="Technical implementation complexity")

class AcademicExpertJudge(dspy.Signature):
    """Academic domain expert judge"""
    text: str = dspy.InputField()
    insights: str = dspy.InputField()
    recommendations: str = dspy.InputField()
    confidence: float = dspy.InputField()
    
    research_rigor: float = dspy.OutputField(desc="Research methodology and rigor")
    evidence_quality: str = dspy.OutputField(desc="Quality and relevance of evidence")
    contribution_significance: str = dspy.OutputField(desc="Significance of research contribution")
```

## Evaluation Metrics

- **Multi-Dimensional Scoring**: Insight quality, recommendation practicality, confidence calibration
- **Domain Expertise**: Specialized judges for business/technical/academic domains  
- **Qualitative Assessment**: Detailed feedback with strengths/weaknesses
- **JSON Structured Output**: Consistent scoring format for optimization
- **Fallback Mechanisms**: Robust parsing for various judge response formats