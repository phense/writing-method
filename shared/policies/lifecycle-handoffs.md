# Lifecycle Handoffs

Every phase consumes current artifacts from disk and names one next phase.

```json
{
  "nodes": [
    "verification-before-completion",
    "documentation-planning",
    "documentation-authoring",
    "documentation-review",
    "tutorial-video-scripting",
    "presentation-video-production",
    "presentation-video-review"
  ],
  "executors": {
    "documentation": "documentation-authoring",
    "presentation-video": "presentation-video-production"
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
    },
    {
      "from": "tutorial-video-scripting",
      "to": "presentation-video-production",
      "artifact": "accepted script: video.json, script/script.md, src/scenes.json, src/narration.json, pronunciation.json",
      "completion_guard": "script check without errors and author acceptance before any voicing"
    },
    {
      "from": "presentation-video-production",
      "to": "presentation-video-review",
      "artifact": "rendered file with out/measure.json, check stills and captions"
    },
    {
      "from": "presentation-video-review",
      "to": "verification-before-completion",
      "artifact": "review.md in the video project",
      "completion_guard": "every check still inspected, measurement passed and no open Critical or Important findings"
    }
  ],
  "retry_transitions": [
    {
      "from": "documentation-review",
      "to": "documentation-authoring",
      "condition": "actionable findings returned for affected chunks",
      "artifact": "docs/writing/<doc-id>/review.md findings",
      "preserves": "accepted chunks and stable chunk IDs"
    },
    {
      "from": "presentation-video-review",
      "to": "presentation-video-production",
      "condition": "findings on picture, sound or file",
      "artifact": "review.md findings",
      "preserves": "accepted sound files and unaffected scenes"
    },
    {
      "from": "presentation-video-review",
      "to": "tutorial-video-scripting",
      "condition": "findings on content, sources or wording",
      "artifact": "review.md findings",
      "preserves": "unaffected scenes and the pronunciation list"
    }
  ]
}
```

Reader-facing documentation follows [writing depth](writing-depth.md). A standalone document uses documentation-authoring and self-review; a set uses planning, authoring and review. Playbook findings return to the invoking writing owner.

A narrated tutorial video follows scripting, production and review. Nothing is voiced before the script check passes and the author accepts the script; a video is ready only after the review's delivery gate. Review findings return to the phase that owns them, and accepted sound is kept.
