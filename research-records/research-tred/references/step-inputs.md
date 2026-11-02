# Step Inputs, Outputs, and Error Tracing

T/R/E/D classify content; research steps classify actions. A step may use selected versions from several areas. Predictions, theory–evidence comparisons, and other reasoning outputs remain in the Episode, linked to TRED by reference.

## Trigger input boundaries

| Step | Main inputs | Distinct output |
|---|---|---|
| Literature search | Candidate lens, focal phenomenon, necessary background | Queries, scope, sources |
| Theory extraction | Available original literature | Abstract arguments, mechanisms, scope |
| Case predictions | Saved arguments, necessary case background | Predictions, reasoning, supportive/contrary criteria |
| Empirical comparison | Fixed predictions, specific material versions | Observations, both sides of evidence, gaps |
| Trigger assessment | Arguments, predictions, comparisons | Assessments, grounds, residual explanatory demands |

Follow theory-first execution: only necessary background before prediction, without scanning empirical sources, old Findings, or case outcomes to choose theories/expectations. Disclose supplied hunches and prior exposure; do not claim blindness. R kind labels help select background but do not prove the content is free of outcomes.

## Input manifest

input-selection.json explicitly identifies episode_id, step_id, run_id; input_objects area/object_id/version/role; input_artifacts project-relative paths/roles; known_observation_exposure; previous_step_ref. Candidates may be inputs with their status explicit, never automatically called adopted.

freeze-inputs resolves selected metadata/content and SHA-256, binding other necessary artifacts too. It creates a research-step-input/v1 manifest and an immutable index snapshot alongside it. It does not read unselected full text, change the index, or execute research. File reading/hashing does not establish AI comprehension; actual_read_refs in the result records actual reading.

Inputs bind exact versions rather than mutable latest. Later current-index changes do not retarget an old manifest. check-inputs verifies the frozen snapshot, metadata, and selected bytes without treating a newer current-index hash as invalidating the old step.

## Outputs and diagnosis

Use step-result.json for input_manifest_ref, output files/versions/hashes, actual_read_refs, reasoning grounds, conditions checked, limitations, status, and history_event_id. Outputs may link arguments, predictions, and comparisons without rewriting the same content. Unexecuted/unsupported work stays partial/blocked rather than fabricated success.

History details.step_refs identifies manifests only; complete step content stays in the Episode. When TRED adopts a step result, register an object referencing that immutable artifact and its History link, rather than copying full text.

Trace backward: assessment → comparison → prediction → theoretical argument → original source. Check input versions, reasoning, applicability, and contrary grounds at each step. After upstream revision, identify affected downstream work; mark it complete only after actual rechecking.

Content categories, input manifests, and isolated execution contexts are different levels of separation. This version supplies the first two, not memory erasure, new-session isolation, background scheduling, or automatic reasoning-quality guarantees.
