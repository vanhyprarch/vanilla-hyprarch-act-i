# SPDX-License-Identifier: GPL-2.0-only
"""Shared, reviewed application metadata; never contains server credentials."""
from dataclasses import dataclass
import json
from pathlib import Path
import re

CATALOG_PATH = Path(__file__).resolve().parents[1] / "config" / "apps.json"


@dataclass(frozen=True)
class Application:
    id: str
    name: str
    subtitle: str
    flatpak_id: str
    workspace: int
    window_class: str = ""


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, Application]:
    data = json.loads(path.read_text())
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported application catalog version")
    result = {}
    workspaces = set()
    for entry in data["applications"]:
        app = Application(**entry)
        if not re.fullmatch(r"[a-z][a-z0-9-]*", app.id):
            raise ValueError("Invalid application name")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]*(?:\.[A-Za-z0-9_-]+){2,}", app.flatpak_id):
            raise ValueError("Invalid Flatpak application ID")
        if app.window_class and not re.fullmatch(r"[A-Za-z0-9_.-]+", app.window_class):
            raise ValueError("Invalid application window class")
        if type(app.workspace) is not int or app.workspace < 2:
            raise ValueError("Application workspaces must be integers starting at 2")
        if app.id in result or app.workspace in workspaces:
            raise ValueError("Application names and workspaces must be unique")
        result[app.id] = app
        workspaces.add(app.workspace)
    return result
