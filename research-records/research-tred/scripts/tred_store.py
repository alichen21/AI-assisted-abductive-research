#!/usr/bin/env python3
"""Inspect portable TRED and freeze step inputs; never apply official State changes."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys

INDEX_SCHEMA = "research-tred/v1"
OBJECT_SCHEMA = "research-tred-object/v1"
INPUT_SCHEMA = "research-step-input/v1"
STATUSES = {"candidate", "pending_review", "adopted", "superseded", "withdrawn"}


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def path_at(root, ref):
    root = root.resolve()
    if not isinstance(ref, str) or not ref or "\\" in ref or ":" in ref:
        raise ValueError("Expected a portable project-relative path")
    part = Path(ref)
    if part.is_absolute() or ".." in part.parts:
        raise ValueError("Path escapes project")
    path = (root / part).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Symlink escapes project")
    return path


def bind(root, ref):
    path = path_at(root, ref)
    if not path.is_file():
        raise ValueError("Missing file: " + ref)
    return {"ref": ref, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected string " + label)
    return value


def object_key(item):
    if not isinstance(item, dict) or item.get("area") not in {"T", "R", "E", "D"}:
        raise ValueError("Expected T/R/E/D object reference")
    identifier = nonempty(item.get("object_id"), "object_id")
    version = nonempty(item.get("version"), "version")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", identifier):
        raise ValueError("Invalid object_id")
    if not re.fullmatch(r"v[0-9]{3,}", version):
        raise ValueError("Expected explicit version such as v001; latest is not a version")
    return item["area"], identifier, version


def catalog(index):
    if not isinstance(index, dict) or index.get("schema") != INDEX_SCHEMA:
        raise ValueError("Unrecognized TRED schema; use the existing project adapter")
    nonempty(index.get("project_id"), "project_id")
    if type(index.get("state_version")) is not int or index["state_version"] < 0:
        raise ValueError("state_version must be a nonnegative integer")
    nonempty(index.get("history_ref"), "history_ref")
    if not isinstance(index.get("objects"), list) or not isinstance(index.get("current"), list):
        raise ValueError("Expected object catalog and current version lists")
    result = {}
    for item in index["objects"]:
        key = object_key(item)
        if key in result:
            raise ValueError("Duplicate object version: " + str(key))
        for field in ("kind", "title", "metadata_ref"):
            nonempty(item.get(field), field)
        if item.get("status") not in STATUSES:
            raise ValueError("Invalid catalog status")
        result[key] = item
    chosen, identities = set(), set()
    for item in index["current"]:
        key = object_key(item)
        if key not in result or result[key]["status"] != "adopted":
            raise ValueError("Current version must exist and be adopted")
        if key[:2] in identities:
            raise ValueError("An object has multiple current versions")
        chosen.add(key)
        identities.add(key[:2])
    if any(item["status"] == "adopted" and key not in chosen for key, item in result.items()):
        raise ValueError("Adopted versions must be listed in current")
    focus = index.get("focus")
    if not isinstance(focus, dict):
        raise ValueError("Expected focus object")
    for name, kind in (("research_question", "research_question"), ("hunch", "research_hunch")):
        if focus.get(name) is not None:
            key = object_key(focus[name])
            if key not in chosen or key[0] != "R" or result[key]["kind"] != kind:
                raise ValueError("Focus must reference the appropriate adopted R object")
    return result


def load_index(root, ref):
    if (root / "TRED.json").exists() or (root / ".abduction.lock").exists():
        raise ValueError("Existing native project: proposal_only; use its configured schema and writer")
    index = read(path_at(root, ref))
    return index, catalog(index)


def metadata(root, item):
    value = read(path_at(root, item["metadata_ref"]))
    if not isinstance(value, dict) or value.get("schema") != OBJECT_SCHEMA:
        raise ValueError("Unrecognized object metadata schema")
    if object_key(value) != object_key(item) or value.get("kind") != item["kind"]:
        raise ValueError("Catalog and object metadata disagree")
    content = bind(root, value.get("content_ref"))
    if content["sha256"] != value.get("content_sha256"):
        raise ValueError("Object content changed: " + value["content_ref"])
    nonempty(value.get("history_event_id"), "history_event_id")
    if not isinstance(value.get("derived_from"), list) or not isinstance(value.get("source_refs"), list):
        raise ValueError("Expected derived_from and source_refs lists")
    return value


def history_events(root, ref):
    path = path_at(root, ref)
    if not path.exists():
        return {}
    data = path.read_bytes()
    if data and not data.endswith(b"\n"):
        raise ValueError("History has an unterminated line; preserve it")
    result = {}
    for line in data.decode("utf-8").splitlines():
        event = json.loads(line)
        identifier = event.get("event_id") if isinstance(event, dict) else None
        if not isinstance(identifier, str) or not identifier or identifier in result:
            raise ValueError("Invalid or duplicate History event ID")
        result[identifier] = event
    return result


def event_at(root, identifier, events, warnings):
    if identifier in events:
        return events[identifier]
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", identifier):
        raise ValueError("Invalid pending History event ID")
    pending = path_at(root, "history/outbox/" + identifier + ".json")
    if pending.is_file():
        event = read(pending)
        if event.get("event_id") == identifier:
            warnings.append({"event_id": identifier, "status": "history_pending"})
            return event
    raise ValueError("Missing History event and pending record: " + identifier)


def check(root, index_ref):
    index, objects = load_index(root, index_ref)
    events, warnings = history_events(root, index["history_ref"]), []
    parents = {}
    for key, item in objects.items():
        obj = metadata(root, item)
        parents[key] = []
        previous = obj.get("previous_version")
        if previous is not None and (previous == key[2] or (key[0], key[1], previous) not in objects):
            raise ValueError("Missing or self-referencing previous version")
        if previous is not None:
            parents[key].append((key[0], key[1], previous))
        for parent in obj["derived_from"]:
            if object_key(parent) not in objects or object_key(parent) == key:
                raise ValueError("Missing or self-referencing derived_from object")
            parents[key].append(object_key(parent))
        event = event_at(root, obj["history_event_id"], events, warnings)
        refs = event.get("details", {}).get("object_refs", [])
        if not any(object_key(ref) == key and ref.get("metadata_ref") == item["metadata_ref"]
                   and ref.get("content_ref") == obj["content_ref"] for ref in refs):
            raise ValueError("History does not link back to object version: " + str(key))
        bindings = {x["path"]: x["sha256"] for x in event.get("artifact_bindings", [])}
        for ref in (item["metadata_ref"], obj["content_ref"]):
            if bindings.get(ref) != bind(root, ref)["sha256"]:
                raise ValueError("Object bytes disagree with their creation/revision event: " + ref)
    visiting, visited = set(), set()
    def visit(key):
        if key in visiting:
            raise ValueError("Cyclic object/version lineage")
        if key not in visited:
            visiting.add(key)
            for parent in parents[key]:
                visit(parent)
            visiting.remove(key)
            visited.add(key)
    for key in parents:
        visit(key)
    update = index.get("last_update_event_id")
    if update is not None:
        event = event_at(root, nonempty(update, "last_update_event_id"), events, warnings)
        snapshot_ref = event.get("details", {}).get("index_snapshot_ref")
        if not isinstance(snapshot_ref, str) or snapshot_ref == index_ref:
            raise ValueError("Index update requires a separate immutable index snapshot")
        snapshot_hash = bind(root, snapshot_ref)["sha256"]
        bindings = {x["path"]: x["sha256"] for x in event.get("artifact_bindings", [])}
        if bindings.get(snapshot_ref) != snapshot_hash or bind(root, index_ref)["sha256"] != snapshot_hash:
            raise ValueError("Current index disagrees with its recorded update snapshot")
    elif index["current"] or index["state_version"] > 0:
        raise ValueError("Current selection requires its actual update event")
    return {"status": "valid_with_pending_history" if warnings else "valid", "profile": "portable",
            "object_versions": len(objects), "current_versions": len(index["current"]),
            "warnings": warnings, "limits": "Structure, byte hashes and links only; no approval or research-validity claim"}


def freeze_inputs(root, index_ref, selection, out_ref):
    root = root.resolve()
    index, objects = load_index(root, index_ref)
    snapshot_bytes = path_at(root, index_ref).read_bytes()
    if json.loads(snapshot_bytes) != index:
        raise ValueError("Index changed while selecting inputs; retry with an explicit baseline")
    if not isinstance(selection, dict):
        raise ValueError("Expected input selection object")
    for field in ("episode_id", "step_id", "run_id"):
        nonempty(selection.get(field), field)
    for field in ("input_objects", "input_artifacts", "known_observation_exposure"):
        if not isinstance(selection.get(field), list):
            raise ValueError("Expected list " + field)
    chosen = []
    for request in selection["input_objects"]:
        key = object_key(request)
        if key not in objects:
            raise ValueError("Input version not in catalog: " + str(key))
        nonempty(request.get("role"), "input role")
        item = objects[key]
        obj = metadata(root, item)
        chosen.append({"area": key[0], "object_id": key[1], "version": key[2], "role": request["role"],
                       "status_at_selection": item["status"], "kind": item["kind"],
                       "metadata": bind(root, item["metadata_ref"]), "content": bind(root, obj["content_ref"]),
                       "content_locator": obj.get("content_locator")})
    artifacts = []
    for request in selection["input_artifacts"]:
        artifacts.append(dict(bind(root, request.get("ref")), role=nonempty(request.get("role"), "artifact role")))
    if selection.get("previous_step_ref") is not None:
        bind(root, selection["previous_step_ref"])
    out = path_at(root, out_ref)
    if out.suffix != ".json":
        raise ValueError("Input manifest must end in .json")
    snapshot = out.with_name(out.stem + ".index.json")
    if out.exists() or snapshot.exists():
        raise ValueError("Frozen input files already exist; choose a new run/version")
    packet = {"schema": INPUT_SCHEMA, "created_at": datetime.now(timezone.utc).isoformat(),
              "episode_id": selection["episode_id"], "step_id": selection["step_id"], "run_id": selection["run_id"],
              "index_snapshot": {"ref": snapshot.relative_to(root).as_posix(),
                                 "sha256": hashlib.sha256(snapshot_bytes).hexdigest(), "state_version": index["state_version"]},
              "input_objects": chosen, "input_artifacts": artifacts,
              "known_observation_exposure": selection["known_observation_exposure"],
              "previous_step_ref": selection.get("previous_step_ref"),
              "history_event_id": selection.get("history_event_id"),
              "scope_evidence": "Declared selection and byte binding; not a trace of what the AI actually read"}
    out.parent.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for path, data in ((snapshot, snapshot_bytes),
                           (out, (json.dumps(packet, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))):
            with path.open("xb") as handle:
                created.append(path)
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        check_inputs(root, out_ref)
    except Exception:
        for path in reversed(created):
            path.unlink()
        raise
    return {"status": "frozen", "manifest_ref": out_ref, "input_objects": len(chosen),
            "index_changed": False, "history_written": False}


def check_inputs(root, ref):
    packet = read(path_at(root, ref))
    if not isinstance(packet, dict) or packet.get("schema") != INPUT_SCHEMA:
        raise ValueError("Unrecognized step input schema")
    snapshot = packet["index_snapshot"]
    if bind(root, snapshot["ref"])["sha256"] != snapshot["sha256"]:
        raise ValueError("Frozen index snapshot changed")
    frozen_index = read(path_at(root, snapshot["ref"]))
    objects = catalog(frozen_index)
    if snapshot.get("state_version") != frozen_index["state_version"]:
        raise ValueError("Input snapshot version label changed")
    for item in packet["input_objects"]:
        key = object_key(item)
        if key not in objects or objects[key]["metadata_ref"] != item["metadata"]["ref"]:
            raise ValueError("Input object does not match its frozen catalog")
        if item.get("status_at_selection") != objects[key]["status"] or item.get("kind") != objects[key]["kind"]:
            raise ValueError("Input status/type does not match its frozen catalog")
        obj = metadata(root, objects[key])
        if obj["content_ref"] != item["content"]["ref"]:
            raise ValueError("Input content reference changed")
        for binding in (item["metadata"], item["content"]):
            if bind(root, binding["ref"])["sha256"] != binding["sha256"]:
                raise ValueError("Selected input bytes changed: " + binding["ref"])
    for binding in packet["input_artifacts"]:
        if bind(root, binding["ref"])["sha256"] != binding["sha256"]:
            raise ValueError("Selected artifact changed: " + binding["ref"])
    return {"status": "valid", "manifest_ref": ref, "uses_frozen_index": True,
            "limits": "Does not verify actual reading, reasoning or context isolation"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "check", "freeze-inputs", "check-inputs"])
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--index", default="TRED/index.json")
    parser.add_argument("--selection", type=Path)
    parser.add_argument("--out")
    parser.add_argument("--manifest")
    args = parser.parse_args()
    try:
        root = args.root.resolve()
        if not root.is_dir():
            raise ValueError("Project root must exist")
        if args.action == "inspect":
            if (root / "TRED.json").exists() or (root / ".abduction.lock").exists():
                result = {"status": "proposal_only", "profile": "existing_native", "reason": "Use existing schema and writer; no migration performed"}
            else:
                index, objects = load_index(root, args.index)
                result = {"status": "inspected", "profile": "portable", "state_version": index["state_version"],
                          "object_versions": len(objects), "current": index["current"], "focus": index["focus"]}
        elif args.action == "check":
            result = check(root, args.index)
        elif args.action == "freeze-inputs":
            if not args.selection or not args.out:
                raise ValueError("freeze-inputs requires --selection and --out")
            result = freeze_inputs(root, args.index, read(args.selection), args.out)
        else:
            if not args.manifest:
                raise ValueError("check-inputs requires --manifest")
            result = check_inputs(root, args.manifest)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, allow_nan=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "blocked", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
