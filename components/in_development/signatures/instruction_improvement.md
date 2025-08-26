---
component_type: signature
name: instruction_improvement
version: 1.0.0
description: DSPy signature for improving component instructions
framework: dspy
signature: "context, current_instruction, examples -> improved_instruction"
fields:
  context: 
    type: InputField
    desc: "Component purpose and usage context"
  current_instruction: 
    type: InputField
    desc: "Current component instruction or prompt"
  examples: 
    type: InputField
    desc: "Examples of successful component usage"
  improved_instruction: 
    type: OutputField
    desc: "Enhanced instruction with better clarity and effectiveness"
---

# Instruction Improvement Signature

This signature defines the contract for improving KSI component instructions.

## Input Fields
- **context**: The overall purpose and context of the component
- **current_instruction**: The existing instruction that needs improvement  
- **examples**: Real usage examples showing how the component performs

## Output Field
- **improved_instruction**: An enhanced version that is clearer, more specific, and more effective

## Usage
This signature is used with DSPy optimizers like MIPROv2 to systematically improve component prompts based on real usage data.