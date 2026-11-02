# Unified Research Events and Collaboration Information

## Responsibilities and event selection

Research skills supply professional facts, existing event types, object/versions, and artifacts. Research History produces one research summary, actor/contribution/model information, unified storage, and read-only views. Original protocols still govern theoretical judgments, Finding evaluation, and State approval; the writer makes none of those decisions.

| Actual occurrence | Event to save | Do not additionally create |
|---|---|---|
| Human feedback targeting a known Finding/revision | human_feedback_submitted; details retains evaluation, target, reason, continuation scope | A duplicate research_feedback/research_decision for that feedback |
| AI revises the same Finding | finding_revised; details retains old/new versions, feedback, rationale | A parallel research_revision |
| Prediction freeze/evidence-search start | predictions_frozen / evidence_search_started; preserve baseline references/hashes | A generic research_action describing the same fact |
| Request/scope selection before an Episode | research_request / research_decision, episode_id=null | An empty Episode created for logging |
| Meaningful action without a professional type | research_action with started/completed/partial/blocked | Independent summaries of each low-level read/tool call |

An Accept feedback is its original professional event; seeing it as a collaboration decision does not justify another research_decision. A separately required approval/application outcome is another actual action, linked to the feedback, not the original decision recorded twice.

A request, the action it initiates, and a later revision are different linked facts. For feedback concerning several objects, list targets in one event. If professional protocols require object-specific records, share the actual feedback link rather than independently summarizing it several times.

## Common fields

Preserve envelopes/types without introducing a third schema: Trigger professional events use validate-abductive-trigger/v1; project interactions without a professional event use research-collaboration/v1. New records put common metadata in top-level collaboration and professional content in details.

| Field | Meaning |
|---|---|
| event_id | EV-UUID assigned on first preparation; unchanged across skills/retries |
| record_key | Stable key for the same fact, carried from the entry/caller rather than recomputed from wording |
| timestamp | Recording time with timezone; preserve legacy time semantics/bytes |
| actor | Researcher / AI / System: the research actor, not summary author |
| episode_id | Actual Episode for professional events; null allowed for project-level generic events |
| finding_ids / feedback_ids / revision_ids | Known IDs or [] |
| artifact_refs / artifact_bindings | Project-relative paths and preparation-time SHA-256; detect changes before append |
| details | Professional facts/structured links or immutable artifact references supplied by the research skill |
| collaboration | Common metadata shared by research and collaboration views |

collaboration fields:

- summary: generate the research summary once. Reference an accurate supplied summary; feedback JSON/report displays reference it or reproduce it exactly as a derived display, not a second potentially inconsistent summary.
- rationale: explicitly supplied reasons or null, preserving qualifications, disagreement, and lack of confirmation.
- capture_mode: contemporaneous or reconstructed.
- occurred_at: verifiable actual occurrence time with timezone; null when retrospective time is unavailable, not the present time pretending to be the past.
- source_refs: kind (current_context / message / event / artifact), actual ref, concise note. For visible interaction without an accessible message ID, current_context + ref=null with an accurate note is allowed. Do not invent locators or store full conversations.
- targets: object type, known id/revision, readable label. Before formal IDs exist, use a label and null IDs rather than guessing.
- contribution_role: proposed / executed / reviewed / revised / decided / unknown. Text authorship alone does not establish intellectual origin.
- action_status: proposed / started / completed / partial / blocked / unknown. Starting is not completing, and completing analysis is not human acceptance.
- related_event_ids: known request, feedback, proposal, or revision events. correction must reference its original event; never invent causal chains.
- model: actual research executor's provider, model_id, model_version, requested_model, provenance (runtime / reported / unknown), source_ref. Unknown values null; retain sources for known information. An alias is not a verified snapshot.
- skills: participating skill names, versions, and optional source commits; unknown version=null.
- recorder: summary recorder's actor/model, separate from the research executor; never use the current recorder to fill historical unknowns.

For non-AI actions, executor-model values are normally null; the recorder may still be AI. Record meaningful contributions by different models separately with actual action links. Summaries neither prove approval nor assign contribution percentages.

## Connecting TRED, History, and step artifacts

TRED preserves complete content, old versions, and current pointers; History preserves changes; Episode preserves actual derivations. details.object_refs items contain area (T/R/E/D), object_id, version, metadata_ref, content_ref, role (created/revised/selected/referenced). details.step_refs items contain manifest_ref and role (input/output/comparison). prepare automatically includes object metadata, content, and manifests in artifact_refs/hash bindings without copying their full text into the log.

Object metadata history_event_id identifies initial creation or that version's revision, and the event's object_refs links back. Later adoption is another decision/application event, not a changed creation event. R version/branch relationships live in TRED metadata; History traces who changed them and why.

The same event's summary, rationale, actual model, and contribution are the primary change narrative. TRED may retain necessary content/source notes but should not generate another potentially inconsistent rationale. State-selection events may reference immutable index snapshots, not the mutable current index.json as a permanently unchanged artifact. Reference/hash checks do not prove approval or modify pointers.

## Reference, additions, and duplicate control

1. Check caller event_id/record_key and known history before writing. When target/professional meaning is known, prepare the professional event plus collaboration once rather than a generic summary followed by a professional duplicate.
2. Carry a recorded request's ID/key from the entry to Trigger. Trigger references it; episode_started is a genuinely new action linked to that request.
3. Reference already recorded feedback/revisions. Append linked correction/professional revisions for newly discovered object links, model information, or summary errors; never edit committed bytes.
4. The tool makes identical event_id/content idempotent. With the same record_key/research content but new generated ID/recording time, return the existing event_id without another line. A conflicting payload under the same key fails instead of silently choosing one.
5. Use append's actual returned event_id, not the ID of a draft superseded by an existing event. Different keys receive no semantic deduplication; similar wording cannot merge two genuinely separate requests.

Without a stable source identifier, first prepare creates event_id and its record_key, then callers carry both. Do not regenerate keys at every handoff and claim deduplication. Starts, ends, different feedback, and actual revisions use different event keys.

## One writer and recovery

Follow the project's single canonical History. Independent projects without routing default to history/events.jsonl. For portable research-tred/v1, append/verify/timeline resolve history_ref from TRED/index.json; explicit --log must agree. Unknown index schema, invalid history_ref, or simultaneous native/portable routing fail pending project configuration rather than opening another log. prepare may still save pending outbox; that neither configures routing nor commits history. The sole maintained implementation is [history_store.py](../scripts/history_store.py). Trigger's old path forwards to the installed sibling or source-suite backend rather than maintaining append/lock logic. Old append/verify arguments and new prepare remain available.

Fill actual content from a template in a temporary draft file, then run:

    python3 scripts/history_store.py prepare --root /path/to/project --event /path/to/draft.json
    python3 scripts/history_store.py append --root /path/to/project --event /path/to/project/history/outbox/EV-UUID.json
    python3 scripts/history_store.py verify --root /path/to/project

prepare supports professional/generic drafts, requires collaboration, creates ID/key/recording time, binds artifacts, and exclusively writes outbox. prepared is not committed. append returns appended or already_appended and the actual event_id. Outbox remains for retries; its existence does not indicate commitment.

Legacy professional events without collaboration remain readable/verifiable/retryable as originally saved. Version 0.1.0 inline details summaries also remain compatible. New drafts use top-level collaboration without migration or invented fields. Do not migrate research artifacts, Finding Revisions, or accepted State.

Independent projects retain .validate-abductive-trigger.lock; native projects retain their lock/writer. The inspected native profile accepts --native-helper /path/to/configured/abduction.py implementing locked/events/append_event/read, and existing TRED.json history_ref must match. Other writers require their actual adapters; do not guess APIs or bypass them with another log.

Native operator is research-history and operator_version identifies this shared tool; actual research-skill versions are in collaboration.skills. The writer does not authenticate people, change TRED/State, or rebuild professional State automatically.

If shared code/writer is absent, incompatible, or blocked, preserve pending events with actual IDs/order as history_pending; do not revert to another writer. Retry in known causal/dependency order rather than sorting random UUIDs. Report conflicts, partial lines, or corruption without truncating the original log.

## Two read-only views of the same events

    python3 scripts/history_store.py timeline --root /path/to/project --view research
    python3 scripts/history_store.py timeline --root /path/to/project --view collaboration

research shows professional type, Episode/object, and summary. collaboration shows the same event_id with actor, contribution, executor model, and recorder model. Both show known TRED object/versions and render Markdown in canonical log order without appending, creating a new store, or changing State. Missing legacy metadata is explicitly unrecorded. These are readable timelines, not proof of theoretical validity or complete history.
