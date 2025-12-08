# Directives

This folder contains Standard Operating Procedures (SOPs) written in Markdown.

## Purpose

Directives are natural language instructions that define workflows, like you'd give a mid-level employee. They are living documents that improve over time.

## Structure

Each directive should include:

1. **Goal** - What this directive accomplishes
2. **Inputs** - What information/data is needed
3. **Tools/Scripts** - Which execution scripts to use
4. **Outputs** - What gets produced
5. **Edge Cases** - Common errors and how to handle them
6. **Learnings** - Updated as issues are discovered

## Example Directive Template

```markdown
# [Directive Name]

## Goal
Brief description of what this accomplishes.

## Inputs
- Input 1: Description
- Input 2: Description

## Tools/Scripts
- `execution/script_name.py` - What it does

## Process
1. Step 1
2. Step 2
3. Step 3

## Outputs
- Output 1: Description
- Output 2: Description

## Edge Cases
- **Issue**: Description
  - **Solution**: How to handle

## Learnings
- Date: What was learned
```

## Best Practices

- Keep directives focused on one workflow
- Update with learnings as you discover constraints
- Use clear, actionable language
- Document API limits, timing requirements, etc.
