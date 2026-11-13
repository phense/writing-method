# Retrieval and source ownership

This contract is optional. It applies only when the session has a memory or retrieval tool the author wants used for the story. When no such tool exists, skip this file entirely: every story skill works from the vault's files alone, and nothing in the method requires a store.

The contract is provider-neutral. It names no service, command or tool; map its terms onto whatever the host offers, and where the host cannot do something stated here, fall back to the vault.

## The vault is the authority

The vault is the editable source for fiction. A retrieval store holds derivatives of vault files: searchable, possibly stale, never an independent editor of the story. Retrieval is advisory. A hit locates a passage; the passage on disk decides. An absent hit is not evidence that a fact never existed.

Do not set up bidirectional merging between a store and the vault. Never silently resolve divergent versions; the vault's accepted revision wins, and the derivative is refreshed or labelled stale.

## Three kinds of knowledge

| Material | Scope | Authority |
| --- | --- | --- |
| General craft research | Global or shared, never a story's scope | The original author or source; a stored note is an attributed, fallible summary |
| This method's own rules and references | The installed method files | The current method files |
| A story's canon and chapter summaries | Exactly one story: the vault's Git root | The accepted vault revision and published text |

The scope of story material is the vault's Git root. Each story vault and each study vault is its own Git repository, so that its root is a boundary a tool can resolve; a folder inside another repository is not a separate scope. Keep a nested vault out of its parent repository's index. After the first save, read the result back and confirm that the reported scope is this vault and nothing wider.

Never search across stories to retrieve story facts. If a tool's story-scoped search also returns general material, read the returned scope and kind and keep craft advice apart from canon. Craft guidance is not story canon, and one story's canon is never another story's fact.

## Reading

Read the story's brief, voice sheet, current chapter card and directly linked accepted facts from disk. Use retrieval for discovery inside the vault's scope, then open the original stored material and compare its recorded source path and revision with the file on disk before using it as current canon. Recover original passages for conflicts.

Use the general scope for craft questions. Do not send vault content to an additional outside service for research or summarising unless the author asks for that processing.

## Saving

Save only when the author wants durable storage. Save concise original source notes and reusable synthesis; do not bulk-copy copyrighted text. A craft note carries source URL and author, access date, inspected scope, limits, and whether a rule is source-derived, this method's synthesis or an author choice. Successful storage does not make a note a verified fact.

Every derivative of a vault file carries, in its body where the tool has no dedicated fields: the story ID, the note ID, the source path relative to the vault root, the source revision or content hash, the canon state, story-time validity, the reveal chapter and the derivation date. These are content conventions; do not assume the tool enforces them.

Keep a local manifest in the vault that maps each source path and revision to the identifier the store returned. When updating, address the existing entry instead of creating a second one, then read it back.

Only accepted material is eligible for a canon derivative. If a draft must be stored, label and scope it as a draft and keep it out of accepted-canon retrieval; the caller checks the canon state, because a store may not filter on it. For a first pilot, keep drafts local to avoid ambiguity.

## Drift and recovery

A changed, superseded or deleted source note needs a matching derivative update or an explicit invalidation. Until that happens, consult the vault and label the stored result stale. After an accepted chapter or a repaired canon conflict, list the derivatives that the change touched and refresh them or mark them stale; this is a manual step unless the author has set up something else.

The integrity control for derivatives is the local manifest: source path, content hash and a full read-back at save time. Before relying on a derivative, compare its recorded hash with the current file. When the manifest and the store disagree, the vault file decides and the derivative is rebuilt.

Nothing in this method watches files, harvests chapters automatically or proves a story consistent. A store that returns no conflict has checked nothing.
