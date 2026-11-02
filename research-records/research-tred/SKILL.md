---
name: research-tred
description: "Organize or update TRED research content, versions of research questions/candidate explanations, current adopted pointers, or explicit inputs for a research step. T stores theory; R stores hunches, puzzles, and research questions; E stores candidate explanations; D stores materials and evidence. TRED preserves content/versions and research-history records changes. Does not generate new explanations, perform IBE, or migrate unknown legacy projects."
metadata:
  version: "0.1.0"
---

# TRED Research Content and Versions

TRED stores complete research objects, historical versions, and current adopted pointers. History records who advanced a change, why, with which actual model/skill and contribution. Episode step artifacts preserve specific inputs, derivation grounds, outputs, and limits. Connect them by object/version, event ID, and artifact references without duplicating complete content.

## First use and routing

Read the [content/version protocol](references/content-and-versions.md). If TRED.json, a TRED directory, or a native writer already exists, inspect its actual schema/routing first. Do not create a parallel TRED or guess field mappings. For an unrecognized existing project, propose changes only and retain proposal_only.

When the researcher requests this structure for an identified new project, use the [project template](templates/project/TRED/index.json) to establish TRED/index.json and T/R/E/D directories. Fill the actual project_id (an existing project identifier or new UUID) and existing History route. Never store real research content in a skill installation. Empty directories are valid; do not force candidate explanations, coding, or an evidence database.

Each independently usable/evaluable object has complete Markdown content and JSON metadata. Existing papers, materials, or Episode outputs may be referenced directly to preserve one original and its provenance. The index stores the catalog, statuses, and version pointers, not all full text.

## Content operations

- New object: use the [metadata template](templates/object.json), [index-entry template](templates/index-entry.json), and [content template](templates/object.md). Identify T/R/E/D, object kind, stable ID, specific version, sources, and History event ID.
- Refining the same question: retain object_id, increment its version, and link previous_version. A different question or independent branch gets a new ID with derived_from. Keep R hunch, case_context, puzzle, and research_question distinct; do not overwrite the initial hunch as the final question.
- AI-proposed wording starts as a candidate. Never overwrite version files. index.current identifies adopted versions; focus.research_question points to an adopted R version. A candidate may be an explicitly labeled working input without becoming an accepted premise.
- Important adoption, withdrawal, or question-framing changes: use the [selection-proposal template](templates/selection-proposal.json) for a concrete proposal/proposed index, bound to the old index version/hash, object versions, and an explicit researcher decision. Accepting a Finding does not automatically approve a TRED update. Follow the project's authorized writing process and first preserve an immutable old-index snapshot. Authorization to develop skills is not real research-project approval.

This version supplies structure, templates, and validation, not a general automatic formal-State apply engine. Native projects retain their writer. For the portable structure, present a reviewable index-selection proposal; after explicit confirmation, use the project's established maintenance/adapter process. Missing writing capability, mapping, or approval means proposal_only, never a claim of application.

## Step inputs and error tracing

Read the [step-input protocol](references/step-inputs.md). Use the [input-selection template](templates/input-selection.json) to specify object versions, necessary materials, and roles. The helper's freeze-inputs fixes the manifest, selected file hashes, and then-current index snapshot. Read only what the step needs; disclose prior exposure rather than scanning data to reverse-engineer theory or predictions.

Use the [step-result template](templates/step-result.json) for actual reading scope, outputs, limits, and upstream input manifest. Trace errors backward through “assessment → comparison → prediction → theoretical argument → source” and their versions. After an upstream revision, identify downstream items requiring review without claiming they were revalidated.

An input manifest declares/binds selected files. It neither erases material already seen in the same context nor proves reasoning isolation or research correctness. It does not create predictions, require initial coding, or launch unimplemented explanation generation/IBE.

The [entirely synthetic project](examples/project/SYNTHETIC.md) demonstrates RQ-DEMO-01 v001→v002, an independent RQ-DEMO-02 branch, and History backlinks. Use the [selection example](examples/question-review-selection.json) on a temporary copy. All roles and decisions demonstrate structure, not real research input, proof of model execution, or approval.

## Handoff to unified History

Locate shared research-history by name. Both installed and source paths relative to this skill are ../research-history/SKILL.md. Establish the actual event ID before saving content; metadata history_event_id identifies the creation/revision event. Pass area, object_id, version, metadata_ref, content_ref, and related step manifests to History as details.object_refs/step_refs.

Keep change reasons primarily in that event's collaboration.summary/rationale; the object holds necessary provenance and event references. Reference an existing summary rather than generating another. Content changes, researcher decisions, and actual index application are distinct facts, linked as they occur rather than duplicated as parallel collaboration records.

When History is uncommitted, preserve outbox and mark pending. Do not fill unknown historical model information or copy full chats for traceability. Use the tools below to check links/hashes; a successful check is not human approval or theoretical validity.

## Tools

[tred_store.py](scripts/tred_store.py) uses Python 3.9+ standard library:

    python3 scripts/tred_store.py inspect --root /path/to/project
    python3 scripts/tred_store.py check --root /path/to/project
    python3 scripts/tred_store.py freeze-inputs --root /path/to/project --selection /path/to/selection.json --out episodes/E-ID/steps/S-ID/input-v001.json
    python3 scripts/tred_store.py check-inputs --root /path/to/project --manifest episodes/E-ID/steps/S-ID/input-v001.json

inspect reads index metadata without full content. check validates objects, versions, hashes, current pointers, and History backlinks. freeze-inputs exclusively creates an input manifest and index snapshot without changing the formal index or History. It fixes specific versions rather than silently following later current-index changes.
