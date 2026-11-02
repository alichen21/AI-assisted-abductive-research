# Theory-first execution protocol

This governs Steps 1–4 within one episode. Continue automatically between steps, without new human checkpoints or initial coding.

## 1. Establish background without scanning the case for fitting theories

Before predictions, use the supplied Candidate Lens, focal phenomenon, necessary Case Context (unit, period, actor roles, setting, resource conditions), existing Hunch, and explicit feedback. Preserve the context version and known observation exposure. If background exists only in chat, save the minimal context used as a referenceable artifact rather than scanning the corpus to obtain it.

Do not proactively read the empirical corpus, complete codes, old Findings/assessments, or outcome summaries derived from them to choose fitting theories or select expectations. File inventories, source metadata, and necessary format checks are not evidence analysis. If text conversion occurs first, save the files without loading their full content into theoretical derivation.

When the user has described outcomes, an earlier conversation inspected sources, or a follow-up carries feedback, do not claim independent blindness. Disclose what is known, independently state literature arguments and derive predictions, then recheck sources. Distinguish literature-based retrospective derivation from explanations added after inspecting a particular passage; changing filenames cannot make them prior expectations.

## 2. An abstract argument is an explanation, not a label

First state the argument for a class of events: conditions, actors/constructs, relationships/processes, reasons/mechanisms, temporal logic, expected outcomes, and qualifiers. Leave this case's names, events, and known outcomes for the next step. Retain Explanation IDs; one paper can provide several arguments and several papers can support one, with differences and original locators preserved.

Abstract means the conceptual level, not the paper's Abstract section. Use available theoretical passages from full text; disclose abstract-only access. Separate descriptive findings, author arguments, and analyst synthesis. Concept names or a paper's single empirical story do not substitute for explanatory logic.

## 3. Map each relevant argument to case predictions

Save separate outputs using the [argument template](../templates/theoretical-explanations.md) and [prediction template](../templates/observable-implications.md). Predictions retain Implication IDs.

Explain what theory says, how background features map to its constructs/conditions, and what follows here and why. Predictions include processes and sequences, not only quantitative outcomes. Unverified conditions stay open for checking; do not assume they hold or equate temporary operationalization difficulty with inapplicability.

Specify supportive and contrary criteria. If theory predicts increasing commitment as uncertainty declines, it does not automatically predict equipment investment immediately after a signature. Contrary criteria must challenge an implication the argument actually supports. Flag claims compatible with any outcome as insufficiently discriminating rather than claiming a strong test.

## 4. Preserve a prediction baseline before evidence search

Order: `theoretical-explanations.md` → `observable-implications.md` → `predictions_frozen` → `evidence_search_started` → prediction-level evidence checking.

- predictions_frozen artifact_refs include the two theoretical outputs and actual Case Context used, with writer-bound byte hashes. Details identify Implication IDs, freeze time, observation_exposure, and derivation mode. Episode prediction_baseline can start null; preserve later references through events/completion instead of editing frozen episode.json.
- evidence_search_started details reference freeze_event_id, material scope, and predictions to check. Disclose unverifiable order; never invent a freeze timestamp preceding actual reading.
- Reuse the existing writer/outbox without altering old logs, predictions, or fixtures. history_store.py appends/hash-binds events but does not manage workflow ordering or erase the model's prior knowledge.

## 5. Check both sides for every prediction, then examine unanticipated phenomena

Use the [comparison template](../templates/theory-observation-comparison.md). Record supporting, contrary, mixed, or missing evidence for every prediction, including unmatched ones. Search directions follow prediction meaning, synonyms, and process indicators, rather than only known-outcome keywords. Preserve search scope, read surrounding context, and check contrary and low-frequency material.

Keep applicability, evidence-check results, and theoretical judgment distinct. No evidence found means only no evidence found in this search. Unknown conditions support Unresolved; unmet conditions may imply Scope Issue; material contrary observations under broadly applicable conditions may support Candidate Discrepancy. A compatible observation need not identify the mechanism uniquely, and one supportive quotation does not validate the whole theory.

After this comparison, actively examine residual observations for Candidate Novelty: specify existing arguments' explanatory objects, what remains outside them, why this is an additional explanatory demand, and which relevant/rival studies were checked. Failure to predict a detail is not a prediction that it cannot occur, nor automatic novelty. Do not invent a contrary prior prediction merely to attach an Implication ID. Such a finding may have no prior prediction but must link the argument, original evidence, and comparison rationale.

Save observation-inspired explanations/predictions separately as exploratory/retrospective versions, record the inspiring evidence, then perform supplementary checks. Preserve all five Assessment Types, finding-level evaluation, follow-up episodes, and TRED approval rules.
