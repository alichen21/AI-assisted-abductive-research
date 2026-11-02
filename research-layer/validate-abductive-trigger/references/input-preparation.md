# Direct inputs and material provenance

This skill accepts a candidate lens and raw or existing empirical materials directly. Initial coding, a codebook, and a shared coded base are not prerequisites. This reference defines input binding, reading, and provenance, not another preparation stage.

## Minimum inputs and entry

- Candidate Lens name, Researcher/AI source, and rationale; retain Episode/Feedback and continuation authority for follow-ups.
- Empirical locations and scope: raw files, interviews, extracted webpages, researcher observations, existing codes, or an existing base. Codes and bases are optional.
- Necessary context, unit, and time frame. The Hunch is optional and reused when available.

Missing codes, coding coverage, or a shared base must not block entry. If materials have not arrived, complete available theoretical work and disclose that Step 4 cannot yet assess empirical claims. Preserve unreadable-file limits while using accessible inputs; ask briefly for genuinely needed material.

## Bind inputs without coding first

Initialize with files, provenance, scope, versions/hashes, and necessary context. Use [empirical-inputs.json](../templates/empirical-inputs.json) or an existing inventory; do not require a fully populated template before research. Sources may record source_id, path, sha256, material type, date, availability, and locator method.

Bind raw materials/snapshots through empirical_inputs. An existing evidence_base ID/version can also be referenced; otherwise it is null. Preserve legacy episodes' evidence_base fields and files without migration or history rewriting.

Extract/OCR/transcribe text or establish page/paragraph/timestamp mapping as needed during analysis, preserving originals and derivatives. Do not turn reading support into preliminary corpus-wide labeling or codebook creation.

## Identify sourced observations directly in Step 4

After saving predictions, search sources in batches starting from each prediction, checking support and contrary grounds and preserving events, actors, processes, conditions, outcomes, passages, and uncertainty. Retain predictions with no hits too. Form comparison observations/evidence directly without creating a first-order coding scheme.

Every used observation resolves to source_id/file and a page, paragraph, turn, or timestamp. Evidence IDs may link comparisons and Findings; existing Code IDs are optional. Reading notes and excerpts do not constitute full coding, and every sentence need not receive a label.

Distinguish self-report, reported accounts, analyst inference, and summaries. Summaries can be bounded inputs, not fabricated verbatim sources; do not invent missing text or unrecorded events.

## Reading scope and context capacity

Use [material-review.json](../templates/material-review.json) or a concise record of in-scope, reviewed, pending, unreadable, excluded, and duplicate sources. Track reading, not coding completion. Disclose what was actually inspected; a few retrieved hits are not the corpus.

Store full materials on disk and retrieve pertinent passages/context in batches. Preserve chronology, conditions, ambiguity, negative cases, and cross-batch checks rather than repeatedly compressing summaries.

Follow the [theory-first protocol](theory-first.md): initialize with metadata and necessary background, without scanning materials, codes, old Findings, or outcome summaries to find fitting theories. Extract abstract arguments in Step 2; save predictions and supportive/contrary criteria with predictions_frozen in Step 3; only then search empirical materials prediction by prediction in Step 4. Record prior observation exposure from case knowledge/feedback as retrospective rather than blind. Save observation-inspired implication revisions with their timing and rationale.

## Storage and versions

Distinguish Project Root, Repository Root, and the skill installation. Preserve originals, necessary text mappings, inventory, literature, five-step episode artifacts, candidate-search, Findings, History, and State Proposals. No first-order-codes file or Stage A is required.

```text
research-repository/
  empirical/
    raw-data/
    empirical-inputs.json       # Or an existing source inventory
    material-review.json        # Or concise reading-scope notes
  literature/
  episodes/<episode-id>/
  history/events.jsonl
  state-updates/<update-id>.json
  research-state/              # Existing format only
```

Honor existing routing, including root TRED/history and repository/ artifacts, without parallel canonical logs. Versioned paths/snapshots and hashes make episodes reconstructable. New materials enter new episode bindings without changing old inputs or requiring incremental coding.
