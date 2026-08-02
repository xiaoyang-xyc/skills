# Agent Memory Taxonomy Reference

## The Four Memory Types (CoALA Framework)

### 1. Working / In-Context Memory
- **Scope**: Current session only
- **Storage**: LLM context window
- **Capacity**: Limited by context length (typically 4K-200K tokens)
- **Usage**: Active reasoning, immediate task context
- **Persistence**: None — lost when session ends

### 2. Episodic Memory
- **Scope**: Cross-session event history
- **Storage**: Vector database or temporal knowledge graph
- **Retrieval**: Semantic similarity search
- **Format**: Timestamped event records with outcomes
- **Example entries**:
  - "2025-06-15: Attempted SQL injection on target X using technique Y — failed due to WAF rule Z"
  - "2025-06-18: Used gobuster for directory enumeration — took 15min for 10K wordlist, found 3 endpoints"
  - "Learned: React useEffect cleanup functions prevent memory leaks in component unmounting"

### 3. Semantic Memory
- **Scope**: Persistent factual knowledge
- **Storage**: Structured files (Markdown, JSON), knowledge graph
- **Retrieval**: Direct lookup, keyword search, or similarity
- **Format**: Condensed facts, definitions, rules
- **Example entries**:
  - "JWT tokens should have max 15min expiry for sensitive operations"
  - "Python's asyncio.gather() is preferred over sequential awaits for independent operations"
  - "XX library is deprecated; use YY as replacement since v3.0"

### 4. Procedural Memory
- **Scope**: Behavioral patterns and workflows
- **Storage**: System prompts, skill definitions, checklists
- **Retrieval**: Auto-applied — embedded in agent instructions
- **Format**: Step-by-step workflows, decision trees, rules
- **Example entries**:
  - "Pentest methodology: recon → service scan → vuln scan → exploit → report"
  - "Code review checklist: input validation → auth check → error handling → logging"
  - "React performance: check waterfalls first, then bundle size, then re-renders"

## Memory Selection Decision Tree

```
What to store?
|
+-- Is it a specific event/interaction? --> EPISODIC
|
+-- Is it a fact/rule/definition? --> SEMANTIC
|
+-- Is it a workflow/process/pattern? --> PROCEDURAL
|
+-- Is it temporary task context? --> WORKING (don't persist)
```

## Storage Technology Matrix

| Memory Type | File Format | Search Method | Update Frequency |
|---|---|---|---|
| Episodic | Markdown with frontmatter | Semantic/keyword | After each task |
| Semantic | Markdown or JSON | Direct lookup | Weekly consolidation |
| Procedural | Skill definitions / checklists | Auto-loaded | Monthly review |
| Working | Context window | Always present | Per session |

## Anti-Patterns to Avoid

1. **Storing transient state** — Session-specific context doesn't belong in long-term memory
2. **Storing what code already says** — Don't duplicate README or code comments
3. **Over-growing the index** — MEMORY.md > 200 lines degrades retrieval quality
4. **Storing without structure** — Always use frontmatter for metadata
5. **Never reviewing** — Stale memory is worse than no memory
6. **Storing raw episodes forever** — Consolidate into semantic knowledge regularly
