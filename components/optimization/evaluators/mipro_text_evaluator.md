---
component_type: evaluation
name: mipro_text_evaluator
version: 1.0.0
description: MIPRO-based evaluation metrics for text analysis optimization
author: claude_code
capabilities:
  - mipro_evaluation
  - multi_factor_scoring
  - optimization_metrics
dependencies:
  - components/optimization/signatures/text_analysis_signature
---

# MIPRO Text Analysis Evaluator

This component implements MIPRO evaluation metrics for the TextAnalysisSignature optimization.

## MIPRO Evaluation Implementation

```python
import dspy
from typing import List, Dict, Any
import numpy as np

class MIPROTextEvaluator:
    """Multi-factor MIPRO evaluator for text analysis signature"""
    
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            'confidence_calibration': 0.3,
            'insight_depth': 0.4, 
            'recommendation_specificity': 0.3
        }
    
    def evaluate_example(self, prediction, ground_truth, trace=None) -> float:
        """Evaluate a single prediction against ground truth"""
        scores = {}
        
        # 1. Confidence Calibration Score
        predicted_conf = float(prediction.confidence)
        actual_quality = self._assess_quality(prediction, ground_truth)
        conf_error = abs(predicted_conf - actual_quality)
        scores['confidence_calibration'] = max(0, 1.0 - conf_error)
        
        # 2. Insight Depth Score (word count + keyword density)
        insight_text = prediction.insights
        insight_score = self._score_insight_depth(insight_text, ground_truth.get('domain'))
        scores['insight_depth'] = min(1.0, insight_score)
        
        # 3. Recommendation Specificity Score
        rec_text = prediction.recommendations
        specificity_score = self._score_recommendation_specificity(rec_text)
        scores['recommendation_specificity'] = min(1.0, specificity_score)
        
        # Weighted final score
        final_score = sum(scores[k] * self.weights[k] for k in scores)
        return final_score
    
    def _assess_quality(self, prediction, ground_truth) -> float:
        """Assess actual output quality (0.0-1.0)"""
        # Simple heuristic: longer, more structured responses = higher quality
        text_length = len(prediction.insights) + len(prediction.recommendations)
        length_score = min(1.0, text_length / 500)  # Normalize by 500 chars
        
        # Check for structure (bullet points, numbers)
        structure_score = 0.0
        for text in [prediction.insights, prediction.recommendations]:
            if any(marker in text for marker in ['•', '-', '1.', '2.', ':']):
                structure_score += 0.5
        
        return (length_score + min(1.0, structure_score)) / 2
    
    def _score_insight_depth(self, text: str, domain: str) -> float:
        """Score insight depth based on length and domain relevance"""
        word_count = len(text.split())
        length_score = min(1.0, word_count / 50)  # Target ~50 words
        
        # Domain-specific keywords
        domain_keywords = {
            'business': ['revenue', 'cost', 'market', 'strategy', 'profit', 'roi'],
            'technical': ['system', 'performance', 'scalability', 'architecture', 'implementation'],
            'academic': ['research', 'methodology', 'analysis', 'theory', 'evidence', 'conclusion']
        }
        
        keywords = domain_keywords.get(domain, [])
        keyword_matches = sum(1 for kw in keywords if kw.lower() in text.lower())
        keyword_score = min(1.0, keyword_matches / 3)  # Target 3+ keywords
        
        return (length_score + keyword_score) / 2
    
    def _score_recommendation_specificity(self, text: str) -> float:
        """Score recommendation specificity"""
        # Look for actionable language
        actionable_words = ['implement', 'create', 'develop', 'establish', 'deploy', 'configure']
        action_count = sum(1 for word in actionable_words if word in text.lower())
        action_score = min(1.0, action_count / 2)
        
        # Look for specific metrics or numbers
        import re
        numbers = re.findall(r'\d+', text)
        specificity_score = min(1.0, len(numbers) / 3)
        
        return (action_score + specificity_score) / 2

# Usage with MIPRO
def create_mipro_evaluator():
    evaluator = MIPROTextEvaluator()
    return evaluator.evaluate_example
```

## Training Data Generator

```python
def generate_training_examples(num_examples: int = 60) -> List[Dict]:
    """Generate training examples for MIPRO optimization"""
    examples = []
    
    domains = ['business', 'technical', 'academic']
    
    for i in range(num_examples):
        domain = domains[i % 3]
        
        # Generate domain-specific training data
        if domain == 'business':
            text = f"Q{i//3} business scenario: Revenue analysis and market positioning..."
            target_insights = "Market analysis reveals competitive advantages..."
            target_recs = "Implement pricing strategy adjustments..."
            
        elif domain == 'technical':
            text = f"System architecture document {i//3}: Scalability requirements..."
            target_insights = "System bottlenecks identified in database layer..."
            target_recs = "Deploy caching layer and optimize queries..."
            
        else:  # academic
            text = f"Research paper {i//3}: Methodology and findings..."
            target_insights = "Statistical analysis demonstrates significant correlation..."
            target_recs = "Further research should investigate causal mechanisms..."
        
        examples.append({
            'text': text,
            'domain': domain,
            'target_insights': target_insights,
            'target_recommendations': target_recs,
            'expected_confidence': 0.7 + (i % 3) * 0.1  # Vary confidence
        })
    
    return examples
```

## MIPRO Configuration

- **Optimization Target**: Multi-factor score (confidence + depth + specificity)
- **Training Examples**: 60 examples (20 per domain)
- **Evaluation Metrics**: Weighted composite score
- **Hyperparameters**: Confidence weight=0.3, Insight weight=0.4, Recommendation weight=0.3