# Content, Versions, and Current State

## Three storage locations

| Location | Stores | Does not duplicate here |
|---|---|---|
| TRED | Theory, problems, candidate explanations, materials/evidence, historical versions, current adopted pointers | Full human–AI conversation or complete change narrative |
| History | Action/reason/contribution/model/decision/application summaries and object references | Complete theory/question/material copies |
| Episode steps | Input manifests, derivation grounds, predictions, comparisons, outputs, limits | Another current State or canonical log |

## Portable new-project structure

TRED/index.json uses research-tred/v1. objects lists each version's metadata path, kind, title, and status. current lists adopted object/versions, at most one per stable object. focus.research_question/hunch is null or identifies a corresponding R object in current. Empty T/E/D areas are valid.

Default object-version paths:

    TRED/R/RQ-ID/v001.md
    TRED/R/RQ-ID/v001.json
    TRED/R/RQ-ID/v002.md
    TRED/R/RQ-ID/v002.json

Metadata uses research-tred-object/v1 with area, object_id, kind, version, previous_version, derived_from, content_ref/hash, sources, and history_event_id. Once referenced, metadata/content freeze; corrections create new versions rather than changed old bytes. Status changes live in the index/History, never rewritten metadata pretending a different initial state.

If complete content already exists elsewhere in the project, content_ref may identify that immutable file with content_locator; content_sha256 binds original bytes. Version metadata still uses the indexed path. Papers/interviews/raw sources need not be copied into D; D may hold traceable observations and locators. Mutable referenced originals must first be versioned or use the project's snapshots.

## Four content areas

- T: theoretical perspectives, abstract literature arguments, mechanisms, and scope. Distinguish author claims, synthesis, and analyst inference with source locators.
- R: case_context, research_hunch, puzzle, research_question. Keep neutral background separate from findings/judgments. Initial hunches may evolve while old versions remain.
- E: candidate_explanation addressing the current problem. Literature arguments remain in T and are referenced as explanatory resources, not copied into independently drifting versions. This version does not generate explanations or perform IBE.
- D: empirical_source, observation, evidence. Distinguish original materials, observations, and inference; retain provenance for both supporting and contrary evidence.

## R versions and branches

Focusing, clarifying, or correcting the same question keeps its ID and links previous_version. A separately researchable question gets a new ID with derived_from pointing to its source question/hunch. RQ-01 v002 and RQ-02 v001 encode different relationships; “question 1/question 2” alone confuses sequence with identity.

The initial hunch and later research_question are different objects connected through derived_from. Historical versions coexist. current selects adopted versions and focus selects the main question; other questions may remain candidates.

## Status and updates

Index statuses: candidate, pending_review, adopted, superseded, withdrawn. adopted means the explicitly selected working version, not certified theoretical truth. Every current entry must be cataloged/adopted. Saving or AI use does not automatically adopt a candidate. Replacement may mark a previous adopted version superseded in the new index, while old snapshots retain its earlier status.

Before adding a candidate/changing the index, prepare content/metadata and a proposed index. Formal judgment changes follow project approval rules. A concrete selection proposal identifies before/after current/focus, exact object versions, old index byte hash, grounds, and source events. Preserve snapshots such as TRED/snapshots/index-v000001.json. After actual application, last_update_event_id references an application event binding the snapshot; generating a proposed index does not justify applied.

No general automatic apply is implemented. Missing approval, a changed baseline, unknown schema, or unavailable writer means proposal_only/pending, not direct overwrite of an old TRED.json. No actual State change means no mandatory proposal.

## History backlinks

history_event_id identifies actual initial creation or this version's revision; read full change reasons, execution models, and contributions from that event. Later index-status changes have their own decision/application events rather than rewritten creation events.

History details.object_refs includes area, object_id, version, metadata_ref, content_ref, and role (created/revised/selected/referenced). created/revised events and corresponding metadata reference each other. selected events identify existing objects rather than pretending to create them. Generate each event summary once.

Assign an event ID first, write object files/bind hashes, then use shared History prepare/append. If not committed, retain the same-ID outbox; check reports history_pending. Absence of both log event and matching outbox is a missing-record error, not complete history. check validates creation-event bindings for metadata/content and the current index against the immutable snapshot bound by its actual update event. It never repairs/rewrites them. Validation checks structure and links, not identity, approval, or semantic correctness.
