---
name: research-history
description: "Store research requests, meaningful actions, feedback, revisions, and decisions together with human–AI collaboration information. Reference existing events to avoid duplicate summaries. Track contribution sources, object versions, and verifiable model/skill information; display research progress or collaboration timelines. Does not store full conversations, make research judgments, or modify Research State."
metadata:
  version: "0.3.1"
---

# Research Collaboration History

As the single shared History entry, preserve research events with collaboration information so later inspection can trace changing research understanding and what humans and AI did. Research skills supply professional event types, grounds, object versions, and artifacts. This skill prepares one summary, adds common metadata, and stores the record. Do not create a separate collaboration summary for the same research fact. Use verifiable context and records only; never invent earlier interactions, times, identities, or model versions.

## When and at what granularity

- A researcher establishes or changes a research objective, puzzle, theoretical lens, material scope, question framing, or further-search scope.
- AI starts a research task (recording its actual model/skill), completes meaningful work, proposes a candidate judgment, or revises an artifact following feedback. Record actual obstacles/interruptions; a start is not completion.
- A researcher accepts, challenges, revises, or rejects a judgment, or decides the next action.
- The actual execution model/verifiable version changes within a task; when several models contribute, connect each to its own action.

Use one record per independently meaningful research event. A response may contain several events; do not record every wording exchange, repeated acknowledgment, file read, or search hit as a collaboration event. Methodological queries, sources, and evidence remain in research artifacts, with summaries linking only necessary outputs. Software development or skill-design discussions unrelated to a real research project are not automatically research data.

## Handoff with the caller

Read the [recording protocol](references/recording-protocol.md). Use the [interaction template](templates/interaction-event.json) for project-level interactions without a professional event. When Trigger supplies a professional event, retain its event_type/details and add common collaboration metadata to that same event.

The [synthetic feedback example](examples/feedback-event.json) shows how one human_feedback_submitted event carries both professional evaluation and collaboration information. It illustrates structure, not real feedback or approval; never submit it to a real project.

The caller supplies the project root/existing log/writer route, professional event and grounds, current visible research interaction or an existing summary, known object versions, existing event_id/record_key, and actually available model/skill information. Request only necessary current content, not a full chat export or credentials. Reference the ID/summary of an existing corresponding event; append linked additions/corrections for new context without changing old bytes.

When preparing a summary, distinguish the action, explicitly supplied reasons, results, and unfinished work. Clarify only an unclear feedback target rather than applying it to all Findings. Record requests to continue research separately from approval of formal State changes; recording a decision neither executes it nor proves authorization.

Return the actually stored/referenced canonical event_id, record_key, location, and status, or pending file and obstacle. Callers pass these across skills rather than using an uncommitted duplicate draft's ID. Continue the original task after handoff; routine process summaries do not require individual researcher confirmation. Unknown noncritical metadata stays unknown without blocking authorized research.

## Summaries and contribution attribution

- Store research-related summaries only, not complete prompts, replies, or verbatim feedback. Keep genuinely available message/artifact locators, without creating conversation transcripts for logging.
- Distinguish proposing, executing, evaluating, and deciding. AI drafting does not imply AI originated every idea; accepting an AI suggestion does not make the researcher its proposer.
- Identify the actor in each summary, contribution_role, and related_event_ids linking requests, feedback, or proposals. Record independent contributions separately; do not estimate contribution percentages.
- Distinguish occurrence time from recording time. Mark retrospective capture reconstructed; use null when original time is unavailable rather than substituting the current time.
- Separate the model executing the research action from the model recording the summary. Preserve verifiable provider, model_id, model_version, requested_model, and provenance; unknown values are null. Do not infer versions from product names, dates, or apparent ability, or fill historical unknowns with the current recorder's model.
- Mark user-supplied model information reported and actual runtime metadata runtime. An alias is a known identifier, not a verified underlying snapshot.

## Storage and recovery

TRED stores full content, historical versions, and current adopted pointers. This skill stores change summaries and object/version references, not full theory/question copies. details.object_refs identifies area, object_id, version, metadata_ref, content_ref, and role; details.step_refs identifies Episode input/output manifests. Object metadata history_event_id points back to its creation/revision event. prepare automatically adds these files to artifact hash bindings; reference validation does not approve a State change.

Append to the project's existing single canonical History without overwriting it. For portable TRED/index.json, history_ref defines the canonical route: append/verify/timeline resolve it automatically. An inconsistent explicit --log is rejected rather than creating another log. Leave unknown/conflicting TRED routing pending until project configuration resolves it. Trigger events retain validate-abductive-trigger/v1 and their types; generic project interactions use research-collaboration/v1. Both share top-level collaboration and the same writer. Project-level episode_id is null. Preserve legacy professional events and 0.1.0 inline summaries in details unchanged; read compatibly without migration or fabricated fields.

The [history_store.py](scripts/history_store.py) here is the single maintained writer, using Python 3.9+ standard library. It supports prepare, verify, append, event-ID/record_key idempotency, and artifact hashes. Trigger's old script only forwards here. Follow a project's existing writer adapter/lock instead of opening another log. The writer performs no theoretical analysis, identity authentication, or TRED/State writes, and does not detect semantic duplicates with different keys.

Use timeline --view research or timeline --view collaboration to display two read-only timelines from the same events. They do not create another canonical history or replace formal State/reconstruction. Clearly show unrecorded collaboration information in legacy events.

If a writer is unavailable or rejects a new event, keep the prepared event in the project's outbox as history_pending and retry with the same ID. Correct committed history with an appended correction, never edited bytes. Retrospective summaries use accessible records only and do not claim complete historical coverage. This skill must be called within an active task; it supplies no background capture or complete audit of model calls.
