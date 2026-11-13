# Lifecycle Handoffs

Every phase consumes current artifacts from disk and names one next phase.

```json
{
  "nodes": [
    "verification-before-completion",
    "documentation-planning",
    "documentation-authoring",
    "documentation-review"
  ],
  "executors": {
    "documentation": "documentation-authoring"
  },
  "edges": [
    {
      "from": "documentation-planning",
      "to": "documentation-authoring",
      "artifact": "docs/writing/<doc-id>/plan.md"
    },
    {
      "from": "documentation-authoring",
      "to": "documentation-review",
      "artifact": "drafted chunk files with frontmatter, glossary and asset manifest state"
    },
    {
      "from": "documentation-review",
      "to": "verification-before-completion",
      "artifact": "docs/writing/<doc-id>/review.md",
      "completion_guard": "no open Critical or Important findings at the reviewed revision"
    }
  ],
  "retry_transitions": [
    {
      "from": "documentation-review",
      "to": "documentation-authoring",
      "condition": "actionable findings returned for affected chunks",
      "artifact": "docs/writing/<doc-id>/review.md findings",
      "preserves": "accepted chunks and stable chunk IDs"
    }
  ]
}
```

Reader-facing documentation follows [writing depth](writing-depth.md). A standalone document uses documentation-authoring and self-review; a set uses planning, authoring and review. Playbook findings return to the invoking writing owner.
