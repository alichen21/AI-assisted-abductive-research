# AI-Assisted Abductive Research

This repository develops a **search-based framework** to support abductive research and investigate whether, how, and under what conditions AI can assist abductive theorizing. The skills make research tasks and human–AI interactions available for examination.

## 1. A search-based framework

Development focuses on research skills within three interconnected layers:

| Layer | Focus |
|---|---|
| **L1 — Theory–Problem Construction** | Formulate and revise theory–problem framings. The current **[Validate Abductive Trigger](research-layer/validate-abductive-trigger/SKILL.md)** skill examines puzzles for potential novelty or discrepancy. |
| **L2 — Explanation–Evidence Search** | Develop and revise candidate explanations and engage with supporting and conflicting evidence. Planned skills include **foreign theory translation**, adapting theories from other domains to the focal phenomenon. |
| **L3 — Diagnosis, Search Control, and IBE Evaluation** | Diagnose limitations, guide further inquiry, and compare explanations through **inference to the best explanation (IBE)**. These capabilities are planned for further development. |

The layers represent interconnected research responsibilities; inquiry can move between them as it develops.

## 2. Recording human–AI interaction

**[TRED](research-records/research-tred/SKILL.md)** and **[History](research-records/research-history/SKILL.md)** together provide a research-process record, analogous to a laboratory notebook. They connect evolving theoretical perspectives (T), research problem representations (R), candidate explanations (E), and data and evidence (D) with step-specific inputs and outputs, researcher feedback, revisions, and decisions. Available AI model and skill version information is also recorded.

These records help identify **where and how humans and AI interact**: how a researcher’s hunch guides AI search, how AI findings prompt reconsideration, and how subsequent feedback changes the inquiry. This supports examination of their respective contributions to abductive theorizing, including productive moves and lines of inquiry that are revised or abandoned.

## 3. Current implementation and further development

The implemented research skill is **Validate Abductive Trigger** in L1. It connects literature-based theoretical arguments to preserved case-specific predictions, examines supporting and counter-evidence, and presents provisional assessments for researcher evaluation. A lightweight entry point, TRED, and History support its use and inspection.

Further development will extend L2 through explanation generation and foreign theory translation, and L3 through diagnosis, search control, and IBE. The effectiveness of AI assistance remains to be assessed through research cases and comparative evaluation.

## 4. Building on existing operational capabilities

Supporting capabilities build on existing work. The bundled **Literature Review** skill comes from [K-Dense Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/5f2bc0341354fd5590aef76a533ada1e1e5b4e62/skills/literature-review), with local coverage/recency adaptations in version 1.11.1 under the MIT license. Attribution and version details appear in [Third-Party Notices](THIRD_PARTY_NOTICES.md).

Technical setup and invocation are covered in the [usage guide](docs/USAGE.md).

## 5. Illustrative case

The [Zhang Xue / ZX Moto example](examples/zhang-xue/README.md) includes [29 archived articles and source metadata](examples/zhang-xue/data/README.md) and a [case report](examples/zhang-xue/results/AI_Abductive_Case_Provisional_Findings_Zhang_Xue_EN_v2.docx). The report traces a researcher’s initial hunch through theoretical arguments, observable implications, and empirical comparisons to a refined working research question. Its analytical outcome remains provisional; a confirmed abductive trigger has not been established.
