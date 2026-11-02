# Research State / TRED Update Interface

Existing native TRED projects retain their internal structures. Shared research-tred adds a portable content/version layout for new projects explicitly adopting it. Trigger hands off references and proposals without migrating legacy structures:

`Findings + Human Feedback → State Update Proposal → TRED Adapter → Existing Research State`

## Portable content structure

research-tred 0.1.0 supplies TRED/index.json (research-tred/v1) and T/R/E/D directories. TRED holds content/versions, shared History records who changed them and why, and Episode artifacts preserve derivations. The index contains the catalog, status, current, and focus, not complete text. Do not impose these paths on an unknown native project.

Revise the same R question with stable object_id/new version/previous_version; a new independent question uses a new ID/derived_from. New proposals start candidate. Adoption, withdrawal, or changes to the current question require confirmation tied to exact object versions/index changes. Metadata history_event_id points to creation/revision; History details.object_refs points back to content/metadata. Keep reasons and model information primarily in the event rather than another TRED collaboration narrative.

Input manifests use details.step_refs, binding object versions, file hashes, and the index snapshot. Helpers inspect/check and freeze immutable inputs; they provide no general formal-State automatic apply. Use the project's established maintenance/adapter flow for index updates; missing confirmation/capability means proposal_only.

Locate research-tred by name. Relative to this references directory: installed ../../research-tred/SKILL.md; source ../../../research-records/research-tred/SKILL.md. Trigger can start from raw materials without first organizing all of TRED.

## Mapping Trigger's five steps to shared records

| Execution point | Content/versions | Process and references |
|---|---|---|
| Initialization | Selected R background/hunch/question and main-lens T versions, if present | Preserve Episode baseline/exposure; follow index.history_ref rather than a second log |
| Steps 1–2 | Literature/abstract arguments belong in T. Explanation ID is Trigger's argument identifier, not an E object identifier | Save literature/arguments in the Episode/literature repository; register T by immutable content reference when needed |
| Step 3 | Case predictions stay in the Episode and reference exact T/R versions | predictions_frozen binds predictions, arguments, and background snapshot; later predictions do not replace earlier versions |
| Step 4 | Raw materials, observations, and evidence belong in D; prediction-level comparisons stay in the Episode | Bind frozen predictions and selected D/raw inputs; preserve actual reading scope and both sides of evidence |
| Step 5 and feedback | Findings/Revisions/evaluations stay in the Episode; propose a new R version/branch for question changes | Attach collaboration to the same professional event; adoption/current/focus changes follow a concrete proposal |

E is reserved for candidate-explanation search addressing the focal problem. Trigger does not automatically generate explanations or create E merely to fill all areas. Unregistered raw materials and Episode artifacts remain valid inputs; full TRED registration is not required.

When the project uses step manifests, follow research-tred input-selection/step-result templates for actual inputs/outputs. Episode step_input_manifest_refs/step_result_manifest_refs holds paths. History details.step_refs uses input/output/comparison roles for real manifests, with details.object_refs for known versions. Reference equivalent existing records without parallel documents. Preserve old versions and known exposure; separate files do not erase model memory.

## Compatibility boundaries of an existing native mechanism

One inspected ai-abductive implementation uses root TRED.json, schema_version/state_version, T/R/E/D, history_ref, history/events.jsonl, history/proposals/, snapshots, decisions, and locked propose/review/apply/recover. R.hunch and R.trigger are fields of that implementation only; read them only if the actual project uses that schema, not as a universal future TRED standard.

That native example stores artifacts under repository/ with original path/source validation; new Episode outputs also go there. Preserve all old log lines, event names, and native proposal IDs without migration/overwrite. Development of this interface did not alter that project's formal TRED, schema, or history.

Use [tred-adapter-config.json](../templates/tred-adapter-config.json) to configure actual project files, schema, and writer with relative paths. Do not distribute private machine paths. Without a schema/writer/mapping, stay proposal_only.

## State Update Proposal

Use the [JSON template](../templates/state-update-proposal.json):

- Update ID, source Episode, related Finding/Revision IDs.
- Operation Add / Revise / Withdraw / Confirm: semantic intentions, not literal JSON Patch operations.
- Target: semantic_target, existing_element_id, resolved_path (null when unknown; do not guess).
- Base State: actual location, version, exact byte hash; unknown values null.
- Previous Value and previous_value_known: unknown does not mean absent.
- Proposed Value, Reason, Supporting Artifacts, Human Feedback.
- Approval/Application/Mapping Status, initially Pending / NotApplied / Unmapped.

Not every Episode changes State. A Covered search can have complete History only, but a substantive change in understanding should produce a concrete proposal. Do not force either report-only storage or a State change. Record no-state-change reasoning when applicable.

Freeze the initial proposal. Its statuses describe creation time. Later approval/application uses new events and immutable receipts rather than editing it to Approved. Changed content gets a new Update ID or explicit version, supersedes_update_id, and fresh approval; old approval does not cover changed bytes.

## Lightweight adapter contract

This is an interface contract, not an implemented field mapper or formal TRED writer. A thin adapter over existing project tools can support:

| Operation | Input | Output/checks |
|---|---|---|
| inspect | Routing, State/schema/history configuration | State reference/version/hash, native writer capabilities, unknown elements; read-only, no new TRED |
| prepare_mapping | Immutable proposal, current State, project-defined mapping | Native mapped patch or needs_mapping; preserve unexplained/unmapped semantics |
| validate | Proposal, patch, schema, supporting artifacts | Fresh baseline, consistent Previous Value, valid references and schema/semantics; otherwise blocked |
| request_approval | Concrete proposal, patch, before/after values, source | Reviewable update; never invented researcher consent |
| apply_approved | Approved exact proposal/patch, real authority, native writer | Locked native review/apply and receipt; refuse unknown mappings, changed hashes, stale bases, or absent approval |
| reconcile | Actual native transaction/receipt and records | Verify a completed application and append missing summary without repeating application/version increments |

Return proposal_only / needs_mapping / awaiting_approval / stale_base / blocked / applied. A native project requires a native receipt before applied, using its snapshots/transactions/recover. Portable projects follow research-tred selection proposals and established file-maintenance procedures, preserving approval provenance, old/new index versions/hashes, immutable snapshots, and an application event; do not fabricate native receipts. Without an established process or approval, both remain proposal-only. This suite supplies no general automatic apply engine.

## Approval and provenance

Formal trigger confirmation, rejection of accepted judgments, or Hunch/Problem Representation changes require researcher confirmation. Bind approval to Update ID, proposal SHA-256, mapped/native patch ID/hash when present, real authority_ref, explicit decision, and time. History preserves an accurate approval summary/source reference rather than full conversation; a summary cannot create authority. Approval covers a concrete inspectable change.

Accepting a Finding and approving State writes are separate unless actual researcher wording explicitly approves both for that exact update. actor: Researcher or an approval file cannot manufacture permission. A later reject/defer revokes approval; changed bytes or baseline require renewed review. A proposal or lens search only automatically adds History.

Application records include Update ID, native Proposal/Review/Run IDs, old/new state versions/hashes, reason, artifact references, approval references, and snapshot/transaction receipt, followed by state_update_applied. If a native system already records state_applied, retain it and link the interface receipt through native_event_id without renaming old events.

## The inspected ai-abductive native interface

Its helper provides plan / complete / propose --run ... --patch ... / review --proposal ... --decision approve|reject|defer --actor ... --reason ... --authority-ref ... / apply --proposal ..., with recover for interruptions. Read the actual project's current instructions rather than executing from this outline alone.

Native patches require the producing run's base_version, base_sha256, rationale, alternatives, and JSON Pointer operations. Application validates output bytes, references, native approval, and baseline. A semantic proposal cannot be submitted directly as a native patch. Bind a genuinely completed native run, archive Episode outputs, construct a patch using confirmed mappings, and obtain real approval of the exact native proposal. Never invent a run or invoke review as a substitute for a human decision merely to appear writable.

The event bridge can use that helper's locked/events/append_event to append new native-envelope events to history/events.jsonl only, leaving State writing/approval unchanged. The event bridge exists; actual TRED field mapping and apply automation do not.
