#!/usr/bin/env python3
"""Shared research-event storage and read-only timeline views."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
from uuid import uuid4

SCHEMA = "validate-abductive-trigger/v1"
COLLAB_SCHEMA = "research-collaboration/v1"
VERSION = "0.3.1"


def time_with_zone(value):
    if not isinstance(value, str):
        raise ValueError("Expected ISO timestamp string")
    moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if moment.tzinfo is None:
        raise ValueError("Timestamp requires timezone")


def model_record(value):
    if not isinstance(value, dict):
        raise ValueError("Expected model record; use explicit nulls for unknown values")
    for field in ("provider", "model_id", "model_version", "requested_model", "source_ref"):
        if field not in value or (value[field] is not None and
                                 (not isinstance(value[field], str) or not value[field].strip())):
            raise ValueError("Expected nullable model string " + field)
    if value.get("provenance") not in {"runtime", "reported", "unknown"}:
        raise ValueError("Expected model provenance runtime/reported/unknown")
    known = any(value.get(key) is not None for key in
                ("provider", "model_id", "model_version", "requested_model"))
    if known and (value["provenance"] == "unknown" or not value["source_ref"]):
        raise ValueError("Known model information requires provenance and a source reference")


def collaboration(row):
    """Use common metadata; preserve the 0.1.0 inline summary representation."""
    if "collaboration" in row:
        return row["collaboration"]
    if row.get("event_schema") == COLLAB_SCHEMA:
        return row.get("details")
    return None


def validate_collaboration(row):
    details = collaboration(row)
    if not isinstance(details, dict):
        raise ValueError("Expected collaboration metadata")
    if not isinstance(details.get("summary"), str) or not details["summary"].strip():
        raise ValueError("Expected a nonempty research summary")
    if details.get("capture_mode") not in {"contemporaneous", "reconstructed"}:
        raise ValueError("Expected capture_mode contemporaneous/reconstructed")
    if details.get("occurred_at") is not None:
        time_with_zone(details["occurred_at"])
    if details.get("contribution_role") not in {
            "proposed", "executed", "reviewed", "revised", "decided", "unknown"}:
        raise ValueError("Invalid contribution_role")
    if details.get("action_status") not in {
            "proposed", "started", "completed", "partial", "blocked", "unknown"}:
        raise ValueError("Invalid action_status; starting an action is not completion")
    sources = details.get("source_refs")
    if not isinstance(sources, list) or not sources:
        raise ValueError("Summary requires at least one real source reference")
    for source in sources:
        if not isinstance(source, dict) or source.get("kind") not in {
                "current_context", "message", "event", "artifact"}:
            raise ValueError("Invalid source reference")
        if not isinstance(source.get("note"), str) or not source["note"].strip():
            raise ValueError("Source reference requires a concise context note")
        if source.get("kind") != "current_context" and not source.get("ref"):
            raise ValueError("Non-context sources require a real reference")
        if source.get("ref") is not None and not isinstance(source["ref"], str):
            raise ValueError("Source reference must be a string or null")
    targets = details.get("targets")
    if not isinstance(targets, list):
        raise ValueError("Expected target list")
    for target in targets:
        if not isinstance(target, dict) or not all(
                isinstance(target.get(key), str) and target[key].strip() for key in ("type", "label")):
            raise ValueError("Targets require type and a readable label")
        for field in ("id", "revision"):
            if target.get(field) is not None and not isinstance(target[field], str):
                raise ValueError("Target IDs/versions must be strings or null")
    related = details.get("related_event_ids")
    if not isinstance(related, list) or any(not isinstance(x, str) or not x for x in related):
        raise ValueError("Expected related event ID list")
    if row["event_type"] == "correction" and not related:
        raise ValueError("Correction must reference the original event")
    model_record(details.get("model"))
    recorder = details.get("recorder")
    if not isinstance(recorder, dict) or recorder.get("actor") not in {"AI", "Researcher", "System"}:
        raise ValueError("Expected recorder identity separate from the research actor")
    model_record(recorder.get("model"))
    skills = details.get("skills")
    if not isinstance(skills, list):
        raise ValueError("Expected skill version list")
    for skill in skills:
        if not isinstance(skill, dict) or not isinstance(skill.get("name"), str) or not skill["name"]:
            raise ValueError("Skill record requires name")
        if skill.get("version") is not None and not isinstance(skill["version"], str):
            raise ValueError("Skill version must be a string or null")


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def read_json(text):
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def safe_path(root, value):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        raise ValueError("Expected portable project-relative path")
    part = Path(value)
    if part.is_absolute() or ".." in part.parts:
        raise ValueError("Path escapes project")
    result = (root / part).resolve()
    if not result.is_relative_to(root):
        raise ValueError("Symlink escapes project")
    return result


def validate_event(row):
    if not isinstance(row, dict) or row.get("event_schema") not in {SCHEMA, COLLAB_SCHEMA}:
        raise ValueError("Unsupported research event_schema")
    fields = ("event_id", "event_type", "timestamp")
    if row["event_schema"] == SCHEMA:
        fields += ("episode_id",)
    for field in fields:
        if not isinstance(row.get(field), str) or not row[field].strip():
            raise ValueError("Missing string " + field)
    time_with_zone(row["timestamp"])
    if row.get("actor") not in {"AI", "Researcher", "System"}:
        raise ValueError("Invalid actor; this field does not authenticate authority")
    for field in ("finding_ids", "feedback_ids", "revision_ids", "artifact_refs"):
        if not isinstance(row.get(field), list) or any(not isinstance(x, str) or not x for x in row[field]):
            raise ValueError("Expected string list " + field)
    if not isinstance(row.get("details"), dict):
        raise ValueError("Expected details object")
    for field in ("object_refs", "step_refs"):
        refs = row["details"].get(field, [])
        if not isinstance(refs, list):
            raise ValueError("Expected reference list " + field)
        for ref in refs:
            if not isinstance(ref, dict):
                raise ValueError("Expected structured " + field)
            if field == "object_refs":
                if ref.get("area") not in {"T", "R", "E", "D"}:
                    raise ValueError("Invalid TRED area")
                for key in ("object_id", "version", "metadata_ref", "content_ref"):
                    if not isinstance(ref.get(key), str) or not ref[key].strip():
                        raise ValueError("Missing TRED object reference " + key)
                if ref.get("role") not in {"created", "revised", "selected", "referenced"}:
                    raise ValueError("Invalid TRED reference role")
            elif not isinstance(ref.get("manifest_ref"), str) or not ref["manifest_ref"]:
                raise ValueError("Missing step manifest reference")
            elif ref.get("role") not in {"input", "output", "comparison"}:
                raise ValueError("Invalid step reference role")
    if row.get("record_key") is not None and (
            not isinstance(row["record_key"], str) or not row["record_key"].strip()):
        raise ValueError("record_key must be a stable nonempty string or null")
    if row["event_schema"] == COLLAB_SCHEMA:
        if row["event_type"] not in {"research_request", "research_action", "research_feedback",
                                     "research_revision", "research_decision", "correction"}:
            raise ValueError("Invalid collaboration event_type")
        if row.get("episode_id") is not None and (
                not isinstance(row["episode_id"], str) or not row["episode_id"].strip()):
            raise ValueError("episode_id must be a known ID or null for project-level events")
    if row["event_schema"] == COLLAB_SCHEMA or "collaboration" in row:
        validate_collaboration(row)
    encoded(row)


def read_events(path):
    if not path.exists():
        return []
    data = path.read_bytes()
    if data and not data.endswith(b"\n"):
        raise ValueError("History has an unterminated last line; preserve and inspect it")
    result, seen, record_keys = [], set(), set()
    for number, line in enumerate(data.decode("utf-8").splitlines(), 1):
        row = read_json(line)
        if not isinstance(row, dict) or not isinstance(row.get("event_id"), str):
            raise ValueError("Invalid event at line " + str(number))
        if row["event_id"] in seen:
            raise ValueError("Duplicate event_id at line " + str(number))
        seen.add(row["event_id"])
        key = row.get("record_key")
        if key is not None:
            if not isinstance(key, str) or not key.strip() or key in record_keys:
                raise ValueError("Invalid or duplicate record_key at line " + str(number))
            record_keys.add(key)
        if row.get("event_schema") in {SCHEMA, COLLAB_SCHEMA}:
            validate_event(row)
        result.append(row)
    return result


@contextmanager
def standalone_lock(root):
    path = safe_path(root, ".validate-abductive-trigger.lock")
    with path.open("a+b") as handle:
        if os.name == "nt":
            import msvcrt
            handle.seek(0)
            if not handle.read(1):
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            if os.name == "nt":
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def history_log_ref(root, requested=None):
    """Respect a portable TRED index's canonical log without creating a second one."""
    index_path = safe_path(root, "TRED/index.json")
    if index_path.exists():
        if (root / "TRED.json").exists() or (root / ".abduction.lock").exists():
            raise ValueError("Both portable and native TRED routing exist; configure the project writer first")
        index = read_json(index_path.read_text(encoding="utf-8"))
        if not isinstance(index, dict) or index.get("schema") != "research-tred/v1":
            raise ValueError("Unknown TRED index schema; configure the project writer first")
        configured = index.get("history_ref")
        path = safe_path(root, configured)
        if requested is not None and safe_path(root, requested) != path:
            raise ValueError("Configured log does not match TRED index history_ref; no parallel history")
        return configured
    value = requested if requested is not None else "history/events.jsonl"
    safe_path(root, value)
    return value


def append(root, row, log_ref=None, native_helper=None):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("Project root must exist")
    validate_event(row)
    required_refs = [ref[field] for ref in row["details"].get("object_refs", [])
                     for field in ("metadata_ref", "content_ref")]
    required_refs += [ref["manifest_ref"] for ref in row["details"].get("step_refs", [])]
    if any(ref not in row["artifact_refs"] for ref in required_refs):
        raise ValueError("Object/step files must be bound as artifacts; prepare the event before appending")
    log_ref = history_log_ref(root, log_ref)
    path = safe_path(root, log_ref)
    native = None
    if native_helper:
        if log_ref != "history/events.jsonl":
            raise ValueError("Inspected native profile supports history/events.jsonl only")
        spec = importlib.util.spec_from_file_location("vat_native_history", native_helper)
        native = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(native)
        if not all(callable(getattr(native, name, None)) for name in ("locked", "events", "append_event", "read")):
            raise ValueError("Native helper is incompatible with the inspected writer profile")
        state_path = safe_path(root, "TRED.json")
        if not state_path.is_file() or not path.is_file():
            raise ValueError("Native project must already be initialized")
        lock = native.locked(root)
    else:
        if (root / "TRED.json").exists() or (root / ".abduction.lock").exists():
            raise ValueError("Managed project requires its configured native writer; no parallel history")
        lock = standalone_lock(root)
    with lock:
        history_log_ref(root, log_ref)
        rows = read_events(path)
        event = dict(row)
        bindings = []
        for ref in row["artifact_refs"]:
            artifact = safe_path(root, ref)
            if not artifact.is_file():
                raise ValueError("Missing artifact: " + ref)
            bindings.append({"path": ref, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest()})
        if "artifact_bindings" in row and row["artifact_bindings"] != bindings:
            raise ValueError("Artifact bytes do not match supplied bindings")
        event["artifact_bindings"] = bindings
        for old in rows:
            if old["event_id"] == event["event_id"]:
                if any(encoded(old.get(key)) != encoded(value) for key, value in event.items()):
                    raise ValueError("Event ID already exists with different content; append a correction")
                return {"status": "already_appended", "event_id": event["event_id"]}
        for old in rows:
            if event.get("record_key") is not None and old.get("record_key") == event["record_key"]:
                if record_payload(old) != record_payload(event):
                    raise ValueError("record_key already describes a different event; reference it or append a correction")
                return {"status": "already_appended", "event_id": old["event_id"],
                        "reused_by": "record_key"}
        if native:
            state = native.read(root / "TRED.json")
            if state.get("history_ref") != log_ref:
                raise ValueError("Configured log does not match native history_ref")
            event.update(operator="research-history", operator_version=VERSION,
                         task=event["event_type"], state_version_before=state["state_version"],
                         state_version_after=state["state_version"], input_artifacts=event["artifact_refs"],
                         output_artifacts=[], outcome="recorded")
            native.append_event(root, event)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("ab") as handle:
                handle.write((encoded(event) + "\n").encode("utf-8"))
                handle.flush()
                os.fsync(handle.fileno())
        return {"status": "appended", "event_id": event["event_id"]}


def record_payload(row):
    """Compare research content without generated IDs, record time or native receipt."""
    ignored = {"event_id", "timestamp", "operator", "operator_version", "task",
               "state_version_before", "state_version_after", "input_artifacts",
               "output_artifacts", "outcome"}
    return encoded({key: value for key, value in row.items() if key not in ignored})


def prepare(root, draft):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("Project root must exist")
    if not isinstance(draft, dict) or draft.get("event_schema") not in {SCHEMA, COLLAB_SCHEMA}:
        raise ValueError("Prepare requires a supported research event draft")
    if collaboration(draft) is None:
        raise ValueError("New prepared events require collaboration metadata; old saved events remain readable")
    event = dict(draft)
    event["artifact_refs"] = list(event.get("artifact_refs", []))
    event["event_id"] = event.get("event_id") or "EV-" + str(uuid4())
    event["timestamp"] = event.get("timestamp") or datetime.now(timezone.utc).isoformat()
    event["record_key"] = event.get("record_key") or "event:" + event["event_id"]
    validate_event(event)
    for item in event["details"].get("object_refs", []):
        for field in ("metadata_ref", "content_ref"):
            if item[field] not in event["artifact_refs"]:
                event["artifact_refs"].append(item[field])
    for item in event["details"].get("step_refs", []):
        if item["manifest_ref"] not in event["artifact_refs"]:
            event["artifact_refs"].append(item["manifest_ref"])
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", event["event_id"]):
        raise ValueError("Event ID is not a portable filename")
    bindings = []
    for ref in event["artifact_refs"]:
        artifact = safe_path(root, ref)
        if not artifact.is_file():
            raise ValueError("Missing artifact: " + ref)
        bindings.append({"path": ref, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest()})
    if "artifact_bindings" in event and event["artifact_bindings"] != bindings:
        raise ValueError("Artifact bytes do not match supplied bindings")
    event["artifact_bindings"] = bindings
    ref = "history/outbox/" + event["event_id"] + ".json"
    path = safe_path(root, ref)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        handle.write(encoded(event) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return {"status": "prepared", "event_id": event["event_id"], "outbox_ref": ref,
            "record_key": event["record_key"],
            "history_committed": False}


def timeline(rows, view):
    """Render existing records only; never project or update official Research State."""
    def cell(value):
        return str(value if value is not None else "Not recorded").replace("|", "\\|").replace("\r", " ").replace("\n", " ")

    def model_label(value):
        if not isinstance(value, dict):
            return "Not recorded"
        return (value.get("model_id") or "Model unknown") + " / " + (value.get("model_version") or "Version unverified")

    if view == "research":
        headers = ["Event ID", "Recorded at", "Research event", "Episode / object", "Summary"]
    else:
        headers = ["Event ID", "Recorded at", "Actor / contribution", "Executor model / version", "Recorder model / version", "Object / version", "Summary"]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        meta = collaboration(row)
        if not isinstance(meta, dict):
            meta = {}
        summary = meta.get("summary") or "Legacy event has no collaboration summary; see existing artifacts."
        object_labels = [item["area"] + "/" + item["object_id"] + "@" + item["version"]
                         for item in row.get("details", {}).get("object_refs", [])]
        common = [row["event_id"], row.get("timestamp")]
        if view == "research":
            targets = [target.get("label") for target in meta.get("targets", [])]
            labels = [row.get("episode_id")] + targets + object_labels + row.get("finding_ids", []) + row.get("revision_ids", [])
            values = common + [row.get("event_type"), "；".join(x for x in labels if x) or "Project level / not recorded", summary]
        else:
            actor = (row.get("actor") or "Unknown") + " / " + meta.get("contribution_role", "Not recorded")
            executor_model = model_label(meta.get("model")) if row.get("actor") == "AI" else "Not applicable"
            recorder = meta.get("recorder", {})
            recorder_model = (model_label(recorder.get("model"))
                              if recorder.get("actor") in {"AI", None} else "Not applicable")
            values = common + [actor, executor_model, recorder_model, "；".join(object_labels) or "Not recorded", summary]
        lines.append("| " + " | ".join(cell(value) for value in values) + " |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "append", "verify", "timeline"])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--log", help="Project log path; portable TRED defaults to index.history_ref")
    parser.add_argument("--event", type=Path)
    parser.add_argument("--native-helper", type=Path)
    parser.add_argument("--view", choices=["research", "collaboration"], default="research")
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if not root.is_dir():
            raise ValueError("Project root must exist")
        if args.action in {"verify", "timeline"}:
            path = safe_path(root, history_log_ref(root, args.log))
            if not path.is_file():
                raise ValueError("History does not exist")
            rows = read_events(path)
            if args.action == "timeline":
                print(timeline(rows, args.view))
                return 0
            result = {"status": "valid", "events": len(rows),
                      "limits": "Structure/unique IDs only; no research validity or approval claim"}
        elif args.action == "prepare":
            if not args.event:
                raise ValueError("prepare requires --event")
            result = prepare(root, read_json(args.event.read_text(encoding="utf-8")))
        else:
            if not args.event:
                raise ValueError("append requires --event")
            result = append(root, read_json(args.event.read_text(encoding="utf-8")), args.log, args.native_helper)
        print(encoded(result))
        return 0
    except (ValueError, OSError, ImportError) as exc:
        print(encoded({"status": "blocked", "reason": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
