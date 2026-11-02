---
name: abductive-research
description: "Lightweight navigation for abductive research. Use when a researcher wants to start or continue abductive inquiry or choose the next research action without naming a specific skill. Route to trigger validation or an independent literature task, and use research-history at meaningful points for unified research events and collaboration information. Specific tasks may invoke their skills directly."
metadata:
  version: "0.8.1"
---

# Abductive Research Entry Point

Route the researcher's current objective to an implemented research skill or shared operational capability. Identify and hand off the task; do not repeat research methods, initialize the called skill in advance, or create a separate research-record system.

## Available capabilities

| Layer | Skill/capability | When to use |
|---|---|---|
| Research Layer · L1 | validate-abductive-trigger | Start research and identify a theoretical problem; test whether an existing puzzle/hunch constitutes an abductive trigger; revisit theoretical grounding and explanatory demands when revising a research question. Compare existing theory with observations and actively identify, specify, and examine potential novelty/discrepancy. |
| Operation Layer | literature-review | Independent literature searches, reviews, organization of theoretical sources, or citation checks; also available within Trigger's existing Step 1. |
| Shared Research Records | research-history | Store professional research events and collaboration information together, reference existing events, and display research progress or human–AI collaboration from the same history. |
| Shared Research Content | research-tred | Organize T/R/E/D content and object versions, check current adopted pointers, and prepare fixed step inputs; History records the change process. |
| Operation Layer · optional external capabilities | coding, file reading/OCR, data processing and analysis | Use capabilities actually available in the environment only when needed; this suite does not bundle a coding skill. |

Explanation generation and IBE are not implemented. If explicitly requested, explain the current boundary rather than presenting Trigger validation or a general literature review as those capabilities. If the researcher authorizes general methods, handle that separately and state that it is outside the implemented research skills.

Route to Trigger according to the theoretical problem the researcher wants to address, not keywords alone. “Start research and examine what needs explanation here,” “Does existing theory already explain this puzzle?” and “How should this question change to have theoretical grounding?” can enter Trigger. Scheduling, wording-only question edits, and general reviews do not enter Trigger simply because they mention starting research or a research question. For question revision, Trigger supplies evidence about explanatory coverage, potential triggers, and residual demands; formal changes still follow researcher-evaluation rules.

## Routing and handoff

1. Respect the explicitly named skill and scope. Direct requests for Trigger or a literature review need not pass through this entry or other research stages.
2. For open requests to start/continue research, inspect only necessary context, task/Episode status, and authorization to identify the problem. Do not scan the corpus, repeat coding, derive predictions, or create an Episode merely to select a skill.
3. Locate and read the required SKILL.md by name in the available skill list. Installed skills normally sit alongside this entry: ../validate-abductive-trigger/SKILL.md and ../literature-review/SKILL.md. Use actual discovered paths if different. Source-suite paths relative to this directory are ../../research-layer/validate-abductive-trigger/SKILL.md and ../../operation-layer/literature-review/SKILL.md. Load only the needed capability.
4. Pass the original request, necessary context, artifact locations, and authorization scope. Trigger initializes itself and proceeds through its five steps; its existing instructions govern Literature Review use.
5. Ask one focused question only if missing information would change task selection. Once Trigger is selected, let it handle lens/material inputs under its own rules instead of asking twice.
6. Return results under the called skill's delivery and stopping rules. Trigger runs continuously within an Episode, with researcher guidance between Episodes; do not automatically enter a new main lens, explanation generation, or IBE.

## Operational capabilities and research records

Load research-tred when organizing content, revising question versions, or preparing step inputs. Installed path: ../research-tred/SKILL.md; source path: ../../research-records/research-tred/SKILL.md. TRED stores full objects and versions, History stores changes and contributions, and Episode artifacts store step inputs, derivations, and outputs. Connect them through object/versions, event IDs, and artifact paths; do not copy full content into History or preload all four areas into reasoning context.

For projects using the portable layout, first inspect TRED/index.json metadata, focus/current, and history_ref. Read only task-selected object versions and pass their references with the single History route. The entry does not run a full TRED audit or freeze inputs; execution steps handle those as needed.

A revision of the same R question keeps its ID and adds a version; an independent question/branch gets a new ID and source link. A candidate does not automatically become the current adopted version. Trigger can still start from raw materials without registering everything in TRED first. For an unknown legacy TRED schema, propose changes without migration or bypassing its native writer.

Operational capabilities can run independently or within research skills. Literature tasks do not require Trigger, and Trigger does not require initial coding or a shared coding evidence base. Operational outputs do not automatically confirm a trigger, alter a question, or change accepted judgments.

Follow the project's existing artifacts, History, Research State, and routing. Do not migrate old records or create another State, History, or Episode in this entry. An independent literature task need not initialize a Trigger Episode.

Use research-history as needed when a meaningful request/scope is established, a task starts or changes model, important results/revisions are saved or blocked, or feedback/decisions arrive. Locate it by name: installed ../research-history/SKILL.md; source ../../research-records/research-history/SKILL.md. Pass the project root/writer route, relevant interaction summaries/current visible interactions, known object versions/events, and actually available executor-model/skill metadata. Without an Episode, record a project-level summary rather than creating an Episode for logging.

Carry previously recorded request/feedback event_id and record_key through handoff. When professional objects/types are known, send the facts and common collaboration metadata for one write, rather than a generic summary followed by a duplicate professional event. For Trigger types such as human_feedback_submitted and finding_revised, attach collaboration information to that same event. Use generic request/feedback types only for project-level interactions without a corresponding professional event. Reference committed events directly; append linked additions/corrections under the shared protocol without overwriting them.

Record the summary recorder separately from the actual executor, linking multiple models to their respective actions. Store research-related summaries only, not full conversations. Use research-history for writes and read-only views. Preserve outbox and disclose pending writes rather than repeating research or claiming commitment. Show research progress and collaboration as two views of the same events, not separate histories.

This entry governs selection and use within an active task. It supplies no background scheduler, automatic dependency download, or independent agent process. Identify missing capabilities without pretending they ran or completed.
