# Research Episodes, Human Feedback, and Append-Only History

This protocol organizes Trigger's professional artifacts and events. Shared research-tred defines content/version structure; research-history supplies collaboration metadata and the sole writer. See [templates](../templates/README.md). Fields support interoperability; a complex database is not required.

## IDs, versions, and immutable artifacts

Production records use typed UUIDs, such as E-…, F-…, FB-…, REV-…, EV-…, and U-…. Short E001-style identifiers are for examples. Prefix Explanation/Implication/Comparison IDs with the Episode ID to avoid cross-episode collisions. A Finding ID is project-wide and stable across revisions; each judgment version receives a unique Revision ID.

Each Episode saves:

```text
episodes/<episode-id>/
  episode.json                          # Frozen initial metadata, baselines, input bindings
  request.md                            # Research request/authorization summary, not a full conversation/prompt
  literature-review.md                  # Step 1; may link shared originals/search records
  theoretical-explanations.md           # Step 2
  observable-implications.md            # Step 3; frozen before Step 4
  theory-observation-comparison.md      # Step 4
  candidate-search.md                   # Steps 4–5: candidate formation, checking, revision, disposition
  findings.json                         # Step 5: multiple finding revisions
  assessment.md                         # Complete report for human evaluation
  episode-completion.json               # Final status, step references, limits, Finding IDs
  feedback/<feedback-id>.json            # Subsequent research-feedback summaries, append-only
  revisions/                            # New versions when correction within the Episode is necessary
```

Follow-up Episodes use independent directories. Create a new version when changing a referenced file; never overwrite old bytes. Episode/Finding statuses are snapshots at save time. Derive current status by event replay; a rebuildable current-view file is not an original record. Preserve intermediate outputs for step-level evaluation of inputs, outputs, and later revisions.

## Episode record

Include at least: Episode ID; lens name/source/rationale; search objective; triggering event/feedback; parent Episode and target Findings; raw/existing material IDs, versions, and bindings (plus evidence-base identity if present); Research Context/Hunch references; skill/model/prompt versions (explicitly unknown if unavailable); literature and step artifacts; Finding IDs; Episode Status; timestamp.

Shared research-history adds collaboration summaries. Record the research executor separately from the summary recorder, with available model identifiers, versions, and provenance. Unknown values remain null/unknown; never infer historical information from product names or the current model. Link model changes and independent contributions to their own events. Summarize research goals, limits, and authorization only. Without a genuine prompt version/reference, retain unknown; request.md is not the complete execution prompt. Preserve old Episodes/history and synthetic examples unchanged rather than migrating summaries or claiming compliance with the new protocol.

Projects using research-tred may record tred_baseline index/snapshot references, version/hash, and step_input_manifest_refs/step_result_manifest_refs. Otherwise retain null/[] without making full TRED organization a prerequisite. Register manifest paths only when actually used; reference equivalent existing records rather than creating a second set for compatibility. The current index is mutable, so long-term artifact hash bindings use immutable snapshots. Full input/output manifests stay in the Episode; details.step_refs uses input/output/comparison roles. Complete theory/question content stays in its original file or TRED version, not copied into the log.

Initialize as started. step_completed/step_blocked may record completion, reference to existing work, partial execution, or blocking. On normal delivery, episode_completed carries awaiting_review: execution is complete, researcher evaluation is not. Do not equate that with failure or accepted theory. For actual limits, record partial/blocked and the resumption point. Never mark unexecuted steps complete or record literature_review_completed without a search. Complete execution includes actual candidate-search progress; rejecting the initial hunch alone is insufficient. candidate_search_completed may link the search output; disclose if it was not performed.

A new lens-specific search creates a new Episode. Authorized supplementary checking under the same lens also uses a new Episode to preserve before/after inputs and results. Researchers need not restart internal steps. When literature tools are actually available, call them internally and save the handoff; reading tool instructions is not a successful invocation.

## Prediction baseline and evidence-search order

Under the [theory-first protocol](theory-first.md), record predictions_frozen and evidence_search_started. The former binds arguments, predictions, and actual background files/hashes; the latter references freeze_event_id. details preserves actual order and known exposure; never fabricate timestamps. Record prediction_baseline through an appended event or completion artifact without modifying frozen initial episode.json. Later predictions get a new version and revision rationale.

Findings retain observable_implication_ids referencing specific prediction versions, locatable through comparisons/artifact references. A novelty Finding about an unanticipated phenomenon may have [] instead, but must explain the lack of a prior prediction, relevant explanatory boundaries, and original evidence. Never fabricate a prediction to complete a link. Do not migrate old fixtures or actual history, or claim they followed a later sequencing protocol. The helper does not automatically enforce step order or prediction independence.

## Researcher-facing reports and internal records

assessment.md, literature-review.md, and other Markdown primarily explain substantive content and reasoning to researchers. Finding JSON/events manage IDs, versions, links, and machine reading. Printing protocol fields is not a research report. Map each short review number to stable Finding/Revision IDs in an appendix or presentation-index.json; show readable labels such as Pending review.

For presentation-only changes, save a separate reading version and mapping without changing source reports, Finding JSON, or History bytes. A presentation_created event may mark presentation_only=true. Do not turn formatting feedback into a Finding Challenge/Reject or fictitious theoretical revision. If presentation and linked content disagree, fix the display without silently changing conclusions.

## Finding record

Each revision follows the [finding template](../templates/finding.json), including stable Finding ID, Revision ID, previous Revision ID, source Episode, related lens, description, Assessment Type, theoretical/empirical justification, observable implications, comparisons, literature/evidence references, uncertainty, preliminary relevance when applicable, and Review Status.

assessment_type allows only Covered / Candidate Novelty / Candidate Discrepancy / Scope Issue / Unresolved. review_status allows only Pending / Accepted / Challenged / Rejected / Revision Requested. These are independent: rejecting a novelty judgment does not set assessment_type=Rejected. Only a subsequent AI revision changes theoretical classification.

Candidate Novelty requires novelty_scope, such as lens_specific or broader_search_bounded, with explicit search boundaries. Lens-specific noncoverage does not establish universal novelty. Preliminary Relevance uses who_cares, why, degree, and uncertainty briefly; it is not L3 contribution scoring.

## Human feedback and continuation authority

Store feedback in independent [JSON](../templates/human-feedback.json) and append its event. Include Feedback ID, target Finding/Revision IDs, researcher decision, research-feedback summary, reason, alternative explanation if supplied, suggested next action, and timestamp. Preserve accurate research-related summaries, qualifications, disagreements, and authorization boundaries—not full conversations or verbatim feedback. Keep original_researcher_comments=null in new records for legacy compatibility; use researcher_feedback_summary. Fill source_ref only with a real available locator, and unavailable reasons with null. Do not invent researcher positions. Feedback about several Findings may have professional object links sharing one event. Feedback JSON history_event_id references that event; any displayed summary derives from or exactly repeats collaboration.summary, without a second summarization.

| Human action | Target revision's review_status | Automatically start a next Episode? |
|---|---|---|
| Accept | Accepted | No |
| Challenge | Challenged | Only with an explicit continuation request or applicable prior authority |
| Revise | Revision Requested | Work within requested changes; record authority if a new search is required |
| Reject | Rejected | No |
| Request Further Search | Preserve existing evaluation; otherwise Pending | Yes, within the requested scope |
| Suggest Another Theoretical Lens | Record the suggestion; do not automatically change evaluation | Continue only when explicitly asked to use it; a suggestion alone waits |

“Another theory may explain this; please continue checking” need not name a lens. Summarize feedback, identify the claim, choose one relevant alternative lens (source=AI, linked to Feedback), and complete that authorized follow-up's five steps. Do not extend authority into an autonomous sequence of lens changes.

Accept evaluates a revision only, not a Research State update. A new AI revision starts Pending rather than inheriting Accepted. Feedback/authority must come from real researcher input; actor: Researcher or a CLI parameter does not authenticate it.

## Follow-up and revision

followup_requested links the original Episode, Finding, Feedback, claim, search objective, and continuation authority. The follow-up records these links, why it is supplementing search/changing lens/re-extracting/re-deriving, and whether materials/versions remain the same.

For a changed judgment about the same issue, retain Finding ID, create Revision ID/previous_revision_id, and append finding_revised. Event details include original_finding_id, previous_revision_id, related_feedback_id, followup_episode_id, new_literature_or_explanations, revised_assessment, revision_reason, new_revision_id, and human_review_status. Explain whether the original judgment is supported, modified, or refuted and why.

A different puzzle/observation receives a new Finding ID with related_finding_ids, not a revision masquerading as the old issue. A later researcher Accept/Reject change is new feedback modifying the current view, never deletion of the original decision.

## Professional events and shared History

This skill defines professional meanings, object relationships, and grounds. Shared research-history prepares/references one summary, adds common collaboration information, and stores the event. One human feedback action or AI revision has one professional event, whose metadata also supports collaboration analysis; do not add a parallel generic summary.

Professional events retain validate-abductive-trigger/v1, original types, Episode/Finding/Revision links, theoretical/evidence details, and artifact references. The [event template](../templates/event.json) puts summary, contribution, model, and recorder information in top-level collaboration. Carry event_id/record_key across handoff instead of generating new ones.

Core types include lens_selected, episode_started, literature_review_completed, step_completed, finding_proposed, human_feedback_submitted, followup_requested, finding_revised, finding_accepted, finding_rejected, episode_completed, state_update_proposed, state_update_approved, state_update_applied, and prediction-baseline events. Legacy types remain readable. A single Accept can be human_feedback_submitted with researcher_decision=Accept; do not duplicate it as research_feedback/research_decision or another finding_accepted summary. A required actual State application is a different system action linked to the decision.

- Human feedback: human_feedback_submitted details retains target revision, evaluation, reason, continuation scope, and Feedback reference; collaboration summarizes that same feedback and human evaluation contribution.
- AI revision: finding_revised retains previous_revision_id, related_feedback_id, new revision, and rationale; collaboration records the AI contribution and actual model.
- Prediction freeze/search: predictions_frozen/evidence_search_started retain input hashes, freeze_event_id, and actual order; a generic summary is not a substitute.
- Episode start/end: distinguish completed/partial/blocked and awaiting_review; starting and completing are different linked facts.

Load the actual research-history skill by name. Relative to this references directory, installed path is ../../research-history/SKILL.md; source path is ../../../research-records/research-history/SKILL.md. It defines the sole log/writer, lock, append-only behavior, idempotency, outbox, model provenance, and two read-only views. This skill does not maintain another storage protocol.

[scripts/history_store.py](../scripts/history_store.py) preserves the legacy invocation path but loads only the shared implementation. append/verify parameters remain available; prepare delegates too. Missing shared code causes an explicit error with pending material preserved, never restoration of a second writer/log. Existing projects keep canonical History/native routing; bridges and recovery follow the shared protocol, with State updates under the [TRED interface](tred-interface.md).

## Reconstructing current views

Replay saved order: a new Finding establishes a revision; finding_revised adds a revision linked to previous_revision_id; feedback changes the specified target revision's status. Accept/Reject never applies to a later unknown revision. Project proposal/approval/application separately—Accepted on a Finding is not proposal approval. Timestamps explain context; log line order governs replay. Late feedback targets its original revision without rewriting newer evaluation.

See [iteration.md](../examples/iteration.md) and its [events](../examples/iteration-project/history/events.jsonl).
