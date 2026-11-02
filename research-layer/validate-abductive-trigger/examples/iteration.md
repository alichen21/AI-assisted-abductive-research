# Complete two-episode iteration example

> Legacy workflow fixture: its codes and Stage A outputs are historical existing inputs, not current prerequisites. Without codes, follow [direct entry](direct-entry.md). The recorded artifacts and events below remain unchanged.


**All case materials, interviews, and explanatory passages are synthetic. No actual external literature search or formal TRED write occurred.** The researcher is a demonstration role, not real approval authority. Signaling/real-options passages illustrate interfaces and revision records, not scholarly claims.

This English package contains a separately localized synthetic fixture. Its source text, fictional comments, and descriptions are English translations; artifact bindings and the derivative event log were generated for those translated bytes. The original Chinese fixture and all real research histories remain unchanged.

[Example project](iteration-project/empirical/evidence-base.json) includes independent Stage A outputs, two episodes with five-step files, two revision-specific feedback records, 22 appended events, and a pending unmapped State proposal.

## Workflow

```text
Independent Stage A (already complete in this example)
Raw materials → First-order Codes → EB-DEMO/v1
                                      │ reuse without recoding
Researcher-provided lens: Signaling    ↓
E001: review → extract → derive → compare → Preliminary Assessment
                                      ↓
F001/REV001: Candidate Novelty (lens-specific), Pending
F002/REV-F002-001: Unresolved, Pending
                                      ↓
FB001 challenges F001/REV001 and explicitly requests alternative checking
                                      ↓
AI selects one alternative primary lens: Real options (source=AI)
E002: full follow-up linked to E001 + F001 + FB001
                                      ↓
Same F001/new REV002: Covered, Pending; REV001 preserved
                                      ↓
FB002 accepts F001/REV002 but says not to change formal State
                                      ↓
Current F001: Covered/Accepted; F002 remains Unresolved/Pending
U001: inspectable suggestion, Pending/NotApplied/Unmapped
Stop automatic search and await the researcher
```

## Inspect each step

| Content | E001 | E002 |
|---|---|---|
| Initial inputs, provenance, evidence version, prior exposure | [episode.json](iteration-project/episodes/E001/episode.json) | [episode.json](iteration-project/episodes/E002/episode.json) |
| Literature handoff and limitations | [literature-review.md](iteration-project/episodes/E001/literature-review.md) | [literature-review.md](iteration-project/episodes/E002/literature-review.md) |
| Structured explanations | [theoretical-explanations.md](iteration-project/episodes/E001/theoretical-explanations.md) | [theoretical-explanations.md](iteration-project/episodes/E002/theoretical-explanations.md) |
| Contextualized implications | [observable-implications.md](iteration-project/episodes/E001/observable-implications.md) | [observable-implications.md](iteration-project/episodes/E002/observable-implications.md) |
| Theory–observation comparison | [comparison](iteration-project/episodes/E001/theory-observation-comparison.md) | [comparison](iteration-project/episodes/E002/theory-observation-comparison.md) |
| Findings and assessment | [findings.json](iteration-project/episodes/E001/findings.json), [assessment.md](iteration-project/episodes/E001/assessment.md) | [findings.json](iteration-project/episodes/E002/findings.json), [assessment.md](iteration-project/episodes/E002/assessment.md) |
| Researcher feedback | [FB001](iteration-project/episodes/E001/feedback/FB001.json) | [FB002](iteration-project/episodes/E002/feedback/FB002.json) |

E001 claims noncoverage within its reviewed lens, not across all literature. FB001 supplies a future-options lead and requests continuation, authorizing E002 without manual launches between internal steps. E002 has already seen observations/feedback and explicitly derives implications retrospectively.

REV002 does not replace E001/findings.json. REV001, original feedback, and new explanations remain independently inspectable. F002 receives no feedback and is unaffected by F001 acceptance. FB002 does not authorize State application.

## Append-only log example

The complete parseable [history/events.jsonl](iteration-project/history/events.jsonl) includes finding_proposed → human_feedback_submitted → followup_requested → finding_revised → finding_accepted → state_update_proposed. Events preserve IDs, timezone-aware timestamps, actor, details, artifact references, and hashes.

Append new events, leaving existing lines unchanged. Revised judgments cite previous_revision_id; changed researcher decisions are new feedback rather than edited comments.

Read-only verification:

```bash
python3 scripts/history_store.py verify --root examples/iteration-project
```

This checks structure and IDs, not theoretical validity.

## State Update Proposal example

[U001.json](iteration-project/state-updates/U001.json) proposes retaining a bounded explanation of deferred investment. No formal State or team-approved mapping exists here: resolved_path and baseline version/hash are null, previous_value_known=false.

approval_status=Pending, application_status=NotApplied, mapping_status=Unmapped. The event binds the exact proposal hash. No state_update_approved/applied exists; Finding Accepted does not imply State updated.

## Scope of the example

It demonstrates stage separation, version reuse, intermediate artifacts, multiple findings, revision-specific feedback, stable-ID revision, append-only history, and no unapproved State write. It does not establish external skill integration, theoretical novelty, saturation, or contribution. Real research requires actual materials and search execution.
