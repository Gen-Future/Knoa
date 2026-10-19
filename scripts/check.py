"""Checks for the preparation stage; no product runtime is selected."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

if sys.version_info < (3, 11):
    raise SystemExit("Repository checks require Python 3.11+; select that interpreter before creating .venv")

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def contract_dir():
    schemas = list(ROOT.glob("contracts/**/parse-result.schema.json"))
    if len(schemas) != 1:
        raise ValueError("Expected exactly one active draft schema; update tooling for more versions")
    return schemas[0].parent


def validate_result(result, schema):
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(result)]
    if errors:
        raise ValueError("; ".join(errors))
    ids = set()
    for item in result["evidence"]:
        if item["id"] in ids:
            raise ValueError("Duplicate evidence ID")
        ids.add(item["id"])
        location = item["location"]
        if location["kind"] == "text" and location["end"] <= location["start"]:
            raise ValueError("Text range must be non-empty and forward")
        if location["kind"] == "time" and location["end_ms"] <= location["start_ms"]:
            raise ValueError("Time range must be non-empty and forward")


def check_contract():
    directory = contract_dir()
    schema = json.loads((directory / "parse-result.schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    source = (directory / "examples/source.txt").read_bytes()
    original = source.decode("utf-8")
    for name in ("success", "failed"):
        result = json.loads((directory / f"examples/{name}.json").read_text())
        validate_result(result, schema)
        if result["source"]["content_sha256"] != hashlib.sha256(source).hexdigest():
            raise ValueError(f"{name}: source digest mismatch")
        for item in result["evidence"]:
            location = item["location"]
            if location["kind"] == "text":
                start, end = location["start"], location["end"]
                if end > len(original) or original[start:end] != item["text"]:
                    raise ValueError(f"{name}: source text/location mismatch")

    manifest_file = ROOT / "contracts/knoa-parse/UPSTREAM.json"
    if manifest_file.exists():
        manifest = json.loads(manifest_file.read_text())
        if manifest["version"] != schema["properties"]["schema_version"]["const"]:
            raise ValueError("Snapshot version mismatch")
        actual_files = {
            str(path.relative_to(directory))
            for path in directory.rglob("*") if path.is_file()
        }
        if set(manifest["files"]) != actual_files:
            raise ValueError("Snapshot manifest must cover every contract file exactly")
        for relative, expected in manifest["files"].items():
            actual = hashlib.sha256((directory / relative).read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError(f"Snapshot drift: {relative}; update through Parse")


def repository_files():
    output = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
    )
    return sorted({
        ROOT / name.decode("utf-8") for name in output.split(b"\0") if name
    })


def main():
    failures = []
    paths = repository_files()
    for path in paths:
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if path.suffix not in {".md", ".json", ".yml", ".yaml", ".txt", ".py"} and path.name not in {
            ".gitignore", ".gitattributes", ".editorconfig"
        }:
            continue
        try:
            raw = path.read_bytes()
            content = raw.decode("utf-8")
            if b"\r" in raw or (raw and not raw.endswith(b"\n")):
                failures.append(f"{relative}: require LF and final newline")
            if any(line.rstrip(" \t") != line for line in content.splitlines()):
                failures.append(f"{relative}: trailing whitespace")
            if path.suffix == ".json":
                json.loads(content)
            if path.suffix in {".yaml", ".yml"}:
                yaml.load(content, Loader=yaml.BaseLoader)
            if path.suffix == ".md":
                prose = re.sub(r"\x60{3}.*?\x60{3}", "", content, flags=re.DOTALL)
                for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", prose):
                    parsed = urlsplit(target.strip("<>"))
                    if parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    destination = (path.parent / unquote(parsed.path)).resolve()
                    if not destination.is_relative_to(ROOT) or not destination.exists():
                        failures.append(f"{relative}: missing/outside-repo link {target}")
        except (ValueError, UnicodeError, yaml.YAMLError) as error:
            failures.append(f"{relative}: {error}")

    try:
        check_contract()
    except (ValueError, KeyError, OSError) as error:
        failures.append(f"Contract: {error}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {len(paths)} repository files; links, syntax, draft contracts and fixtures")


if __name__ == "__main__":
    main()
