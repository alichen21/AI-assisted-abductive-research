# Installation and Usage

See the [README](../README.md) for research purpose and framework. This guide covers installation, invocation, and implementation boundaries.

This is the **English edition of suite 0.8.7**, based on the architecture developed from validate-abductive-trigger-0.4.1-zh.zip. It includes a lightweight entry point, independently callable Trigger, shared literature capability, Research TRED, and Research History. It contains skills only, without plugin configuration.

## Layout and responsibilities

```text
abductive-research/
├── entry/abductive-research/                  Lightweight entry point
├── research-layer/validate-abductive-trigger/ L1 trigger search and validation
├── operation-layer/literature-review/        Shared literature capability, locally adapted K-Dense 1.11
├── research-records/research-history/        Research events, collaboration summaries, model/contribution provenance
├── research-records/research-tred/           T/R/E/D content, versions, and step inputs
├── skills.json                              Suite-maintenance manifest
├── install.py                               Copies the five independent skills
└── THIRD_PARTY_NOTICES.md                    Third-party provenance and licenses
```

Explanation generation and IBE remain future development. Coding, OCR, data processing, and analysis are operational capabilities used when actually available and needed. This edition does not bundle them or make coding a prerequisite for Trigger.

Research History is the shared record entry and single maintained writer. Trigger retains professional events, object versions, prediction baselines, theory/evidence grounds, and human-evaluation semantics. The same event's collaboration holds summary, contribution, executor model, and recorder information; no duplicate generic feedback/revision summary is needed. Two read-only timelines show research progress and collaboration from the same events. Preserve unknown metadata without complete conversations, old-record migration, or changed State-approval rules.

Research TRED stores full research content, versions, and current adopted pointers. History records how those objects change through human–AI interaction. Episode artifacts preserve step inputs, derivations, outputs, and limits. Object metadata history_event_id links to creation/revision events; History object_refs links back to exact versions and step_refs links manifests. Original documents/step artifacts may be referenced without several full-text copies.

## Installation

Source layers organize maintenance. For independent discovery, place the five skill directories side by side in a skills location supported by the host.

From the extracted suite directory, run with Python 3.10+ standard library:

```bash
python3 install.py --dest /your/research-project/.agents/skills
```

Or choose a user-level location:

```bash
python3 install.py --dest ~/.agents/skills
```

The installer copies bundled files only. It does not access the network, install external dependencies, execute research, or alter host settings. Any existing same-name target causes a stop before copying; decide which edition/version to keep first so local modifications are not overwritten. Rerunning the installer is not an upgrade operation.

Alternatively, copy the complete entry/abductive-research, research-layer/validate-abductive-trigger, operation-layer/literature-review, research-records/research-history, and research-records/research-tred directories into the same skills location. Do not install a layer directory as one skill. If new skills are not visible, start a new session or refresh under the host's instructions.

The English and Chinese editions use the same skill identifiers. Install one edition in a given discovery scope, or use a separate project scope for the English edition; do not create competing same-name installations. Producing this package does not replace an existing installation.

## Invocation

- To start/continue research or decide the next action: `$abductive-research`.
- To identify a theoretical problem at research onset, test a puzzle as a potential trigger, or revisit a research question's theoretical grounding/explanatory demands: `$validate-abductive-trigger`.
- For an independent literature task: `$literature-review`.
- For research-process summaries or retrospective recording from verifiable sources: `$research-history`; the entry and Trigger also call it at meaningful points.
- For content organization, question versions, adopted pointers, or step inputs: `$research-tred`.

Trigger remains directly callable. Its History storage depends on shared research-history. The legacy history_store.py path forwards to the same installed backend rather than maintaining a second implementation. Missing shared code means pending handoff and disclosure, not another log. TRED organization is not an additional prerequisite for Trigger.

Natural-language requests can match each skill's description. The entry loads the selected skill as needed without preloading literature, materials, or every operational capability. Direct Trigger calls still use Literature Review within Step 1 under Trigger's scope, without first calling the entry.

Examples: “Start researching this phenomenon and identify what needs explanation,” “Does this puzzle constitute an abductive trigger?” and “Before adjusting my research question, check its theoretical grounding and remaining explanatory demands.” Trigger handles missing lens/material inputs under its original rules. Wording-only question edits or scheduling do not trigger it. An explicit request such as “Use $literature-review to review these theoretical sources” can run independently without a Trigger Episode.

## Current components and integration

- abductive-research 0.8.1 passes selected question/content versions and the single log route; the entry reads necessary metadata rather than all TRED content.
- research-tred 0.1.0 provides four directories/a small index, object/content/step templates, R version/branch rules, and validation/input-freezing helpers. Its entirely synthetic R example is not actual research data.
- research-history 0.3.1 preserves object_refs/step_refs and artifact hashes and resolves portable TRED history_ref automatically, rejecting conflicting routes. Legacy logs remain compatible.
- Trigger 0.4.10 keeps the shortened main instructions, theory-first sequence, complete five steps, two-sided checks, active candidate search, and human evaluation. The research-artifact reuse policy added in 0.4.8 was withdrawn; input, prediction-freezing, and per-Episode artifact protocols follow suite 0.8.3. Each Episode independently conducts and saves its research process. Existing literature arguments belong in T; E is reserved for later focal-problem candidate explanations.
- Event-ID idempotency and same-record_key/same-fact reference/conflict handling remain. Different-key semantic duplicates are not automatically identified; callers must pass actual committed IDs and keys.
- Literature Review 1.11.1 adds recent-literature discovery, breadth checks, and stopping criteria to upstream 1.11. Original hashes and local modifications are separately recorded in upstream.json; the original license is retained.
- This language edition does not conduct real literature searches/Trigger analysis or migrate project records. Older examples remain demonstrations of their recorded schema/version; they do not establish compliance with later summary/sequence protocols. Historical archives and source editions remain separate. Back up local skills before replacing them; this package does not overwrite automatically.

Research History normally receives necessary context at meaningful interactions, forms a summary, and appends to the existing project History. If blocked, it retains outbox as history_pending rather than claiming commitment. It runs within an active task and cannot capture all platform chats or hidden model snapshots. It can also store standalone summaries in an explicitly identified project directory.

## First TRED version: boundaries

The portable layout uses TRED/index.json plus four content directories, with stable IDs/specific Markdown and JSON versions. current/focus selects adopted versions. Refining the same question adds a version; an independent question gets a new ID/derived_from. History holds reasons, models, and contributions; old TRED content remains in historical versions.

Tools provide inspect/check/freeze-inputs/check-inputs, not a general formal-State automatic apply engine. Selection requires a concrete proposal, explicit confirmation, and established project maintenance/adapter flow. Unknown native TRED.json projects remain proposal_only, without migration/direct overwrite. Manifests bind files/snapshots but do not guarantee model-context isolation or reasoning quality. This release supplies skills/templates without initializing or changing actual research projects.

Literature Review's networking, optional CLIs, PDF tools, image generation, and credentials retain upstream requirements. Bundled skill files do not imply those external tools are installed/connected; check actual availability. Trigger retains the defined literature handoff scope and alternatives.

skills.json/upstream.json are maintenance manifests, not a host-standard automatic dependency declaration. Add other operational capabilities only when implemented; do not create empty skills.

## Shared literature maintenance

Standard (Chinese/English), alternative, and benchmark source suites each bundle a copy of Literature Review. Version 1.11.1 is byte-identical across the four suites. Within one installed discovery scope, all conditions resolve the same `literature-review` skill by name. Synchronize the source copies when updating; historical archives do not change automatically. This update changes the operational literature component, not the conditions' research procedures.

## Concise assessment writing

Trigger 0.4.10 requires reading the report guidance before assessment. Ground focal judgments in concrete observation/theoretical expectation comparisons, reasons, and consequential contrary evidence, rivals, or condition gaps; identify evidence that would change a disputed judgment. Usually aim for 500–750 words, adjusted to complexity. Full derivations, all predictions, and two-sided checks remain in the analysis files. A new synthetic short example illustrates the prose without rewriting older records. Alternative and benchmark research/presentation rules are outside this update.
