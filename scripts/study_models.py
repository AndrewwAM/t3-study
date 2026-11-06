#!/usr/bin/env python3
"""Read/validate T3 study-model profiles; never run agents or create study notes."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


class StudyError(ValueError):
    pass


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".t3-study-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


ROLES = ("study_researcher", "study_mermaid_maker", "study_visual_maker")


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise StudyError(f"No se pudo leer {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise StudyError(f"{path} debe contener un objeto JSON.")
    return value


def config_path(workspace: Path) -> Path:
    return workspace.resolve() / "study-models.json"


def load_config(workspace: Path) -> dict:
    path = config_path(workspace)
    if not path.exists():
        return {"schema_version": 1, "environments": {}}
    data = read_json(path)
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1 or not isinstance(data.get("environments"), dict):
        raise StudyError(f"Esquema inválido en {path}; se conservó el archivo.")
    return data


def read_catalog(path: Path) -> dict:
    data = read_json(path)
    # Accept either the capabilities payload or its MCP transport envelope.
    if isinstance(data.get("structuredContent"), dict):
        data = data["structuredContent"]
    elif "providers" not in data and isinstance(data.get("content"), list):
        for item in data["content"]:
            if item.get("type") == "text":
                try:
                    candidate = json.loads(item["text"])
                except (ValueError, KeyError):
                    continue
                if isinstance(candidate, dict) and "providers" in candidate:
                    data = candidate
                    break
    if not isinstance(data.get("providers"), list):
        raise StudyError("El catálogo debe ser la respuesta de orchestrator_capabilities.")
    return data


def validate_profile(profile: dict, catalog: dict) -> list[str]:
    errors = []
    if not isinstance(profile, dict) or not isinstance(profile.get("roles"), dict):
        return ["El perfil debe tener un objeto roles."]
    roles = profile["roles"]
    if set(roles) != set(ROLES):
        errors.append("Define exactamente estos roles: " + ", ".join(ROLES))
    providers = {p["providerInstanceId"]: p for p in catalog["providers"]}
    parent_provider = catalog.get("inheritedProviderInstanceId")
    runtime_mode = catalog.get("runtimeMode")
    for name, target in roles.items():
        if not isinstance(target, dict):
            errors.append(f"{name}: el destino debe ser un objeto.")
            continue
        if target == {"mode": "parent"}:
            continue
        if set(target) != {"providerInstanceId", "model", "options"}:
            errors.append(f"{name}: usa providerInstanceId, model y options, o solamente mode=parent.")
            continue
        pid, model = target["providerInstanceId"], target["model"]
        if not isinstance(pid, str) or not isinstance(model, str) or not pid or not model:
            errors.append(f"{name}: proveedor y modelo deben ser identificadores de texto.")
            continue
        provider = providers.get(pid)
        if not provider or not provider.get("canRunChildTask"):
            errors.append(f"{name}: proveedor {pid!r} ausente o deshabilitado para delegar.")
            continue
        if parent_provider and pid != parent_provider and not provider.get("canRunCrossProviderChildTask"):
            errors.append(f"{name}: {pid} no permite delegación desde el proveedor actual.")
        modes = provider.get("runtimeModes")
        if modes and runtime_mode and runtime_mode not in modes:
            errors.append(f"{name}: {pid} no admite el modo de ejecución actual ({runtime_mode}).")
        selected = next((m for m in provider.get("models", []) if m.get("id") == model), None)
        if selected is None:
            errors.append(f"{name}: {model!r} no aparece en esta instantánea; buscarlo en T3 y ampliar el catálogo antes de validarlo.")
            continue
        options = target["options"]
        if not isinstance(options, dict):
            errors.append(f"{name}: options debe ser un objeto (puede ser vacío).")
            continue
        supported = {o["id"]: o for o in selected.get("options", []) or []}
        for key, value in options.items():
            values = supported.get(key, {}).get("values", [])
            if not any(type(value) is type(allowed) and value == allowed for allowed in values):
                errors.append(f"{name}: opción no soportada {key}={value!r}; valores permitidos: {values}.")
    return errors


def check(workspace: Path, environment: str, catalog: dict) -> dict:
    profile = load_config(workspace)["environments"].get(environment)
    if profile is None:
        return {"status": "setup_required", "config": str(config_path(workspace)),
                "environment": environment, "targets": {}}
    errors = validate_profile(profile, catalog)
    return {"status": "needs_attention" if errors else "ready",
            "config": str(config_path(workspace)), "environment": environment,
            "profile": profile, "errors": errors,
            "targets": {} if errors else {name: target for name, target in profile["roles"].items()
                                          if target != {"mode": "parent"}}}


def save_profile(workspace: Path, environment: str, profile: dict, catalog: dict) -> dict:
    if not environment.strip():
        raise StudyError("Indica el environmentId real de T3.")
    errors = validate_profile(profile, catalog)
    if errors:
        raise StudyError("\n".join(errors))
    if not (workspace.resolve() / "skills/t3-study/SKILL.md").is_file():
        raise StudyError("El workspace debe contener skills/t3-study/SKILL.md.")
    data = load_config(workspace)
    data["environments"][environment] = profile
    atomic_write(config_path(workspace), json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return check(workspace, environment, catalog)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    show = sub.add_parser("show")
    show.add_argument("--environment")
    for name in ("check", "set"):
        p = sub.add_parser(name)
        p.add_argument("--environment", required=True)
        p.add_argument("--catalog", type=Path, required=True)
        if name == "set":
            p.add_argument("--profile", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "show":
            data = load_config(args.workspace)
            result = data if not args.environment else {
                "environment": args.environment,
                "profile": data["environments"].get(args.environment),
                "config": str(config_path(args.workspace)),
            }
        else:
            catalog = read_catalog(args.catalog)
            if args.command == "set":
                result = save_profile(args.workspace, args.environment, read_json(args.profile), catalog)
            else:
                result = check(args.workspace, args.environment, catalog)
        # ASCII JSON also works when Windows redirects stdout using a legacy
        # code page; the editable config itself is always written as UTF-8.
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 2 if result.get("status") in ("setup_required", "needs_attention") else 0
    except (StudyError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
