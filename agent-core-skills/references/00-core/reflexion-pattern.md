# Reflexion Self-Learning Pattern

## Overview

Reflexion (Shinn et al., 2023) is a meta-cognitive architecture where agents learn from mistakes by generating self-critique and storing it in episodic memory for future retrieval.

**Key insight**: Operating at the semantic level (text memory) rather than weight updates, making it interpretable and composable with existing LLM architectures.

## The Reflexion Loop

```
[Attempt Task] --> [Evaluate Result] --> [Generate Reflection]
      ^                                          |
      |____________ [Apply Memory] <______________|
```

### Step 1: Attempt Task
Execute the task using current skills and knowledge. Record the full trace of actions taken.

### Step 2: Evaluate Result
Assess outcome against success criteria:
- **PASS**: Task completed successfully, first attempt
- **PARTIAL**: Task completed with corrections needed
- **FAIL**: Task not completed or produced incorrect result

### Step 3: Generate Reflection
If result is PARTIAL or FAIL, generate structured self-critique:

```markdown
## Reflection: [Task Name] — [Date]

### What I Tried
[Description of approach]

### What Went Wrong
[Specific failure mode]

### Root Cause Analysis
[Why did this happen? Deep analysis]

### What I Should Have Done
[Correct approach]

### Prevention Strategy
[How to avoid this in the future]
```

### Step 4: Store in Memory
Write reflection to appropriate memory file:
- `feedback/` — For error corrections
- `methodology/` — For process improvements
- `patterns/` — For reusable solutions

### Step 5: Apply in Future
Before attempting similar tasks:
1. Search memory for related reflections
2. Load relevant lessons into working memory
3. Adjust approach based on stored insights

## Hierarchical Reflection

For complex tasks, use multi-level reflection:

### Low-Level (Action)
- Individual tool calls or commands
- Example: "This grep pattern missed results because -r wasn't specified"

### Mid-Level (Task)
- Overall task strategy
- Example: "Should have done reconnaissance before attempting exploitation"

### High-Level (Strategy)
- Cross-domain methodology
- Example: "Always verify scope boundaries before testing — applies to all pentests"

## Kolb's Learning Cycle Mapping

| Kolb Stage | Agent Equivalent | Memory Output |
|---|---|---|
| Concrete Experience | Execute task | Episodic record |
| Reflective Observation | Evaluate + critique | Reflection entry |
| Abstract Conceptualization | Extract pattern | Semantic rule |
| Active Experimentation | Apply improved approach | Procedural update |

## Quality Standards for Reflections

### Good Reflection Characteristics
- Specific (names files, commands, exact errors)
- Actionable ("do X instead of Y" not "be more careful")
- Causal (explains why, not just what)
- Tagged (type, source, date, domain)

### Bad Reflection Characteristics
- Vague ("was slow" — how slow? why?)
- Obvious ("should test before deploying" — already known)
- Untagged (hard to retrieve later)
- Duplicated (same lesson learned multiple times — should consolidate)

## Implementation Checklist

After every significant task:

- [ ] Evaluate outcome (PASS / PARTIAL / FAIL)
- [ ] If PARTIAL or FAIL, write structured reflection
- [ ] Tag with type, domain, and source
- [ ] Store in appropriate memory file
- [ ] If 3+ similar reflections exist, consolidate into pattern
- [ ] Update MEMORY.md index if needed
- [ ] Review for index size (keep under 200 lines)
