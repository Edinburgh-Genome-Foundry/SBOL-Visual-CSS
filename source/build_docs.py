from __future__ import annotations

import json
import shutil
from pathlib import Path

from build_css import build as build_css_bundle


def render_templates(repo_root: Path) -> None:
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError as exc:
        raise RuntimeError(
            "jinja2 is required to build the documentation. Install it with 'pip install jinja2'."
        ) from exc

    templates_dir = repo_root / "templates"
    dist_dir = repo_root / "dist"
    icons_json_path = dist_dir / "icons.json"
    
    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates directory not found: {templates_dir}")

    # Load icons data
    icons_data = {}
    if icons_json_path.exists():
        icons_json = json.loads(icons_json_path.read_text(encoding="utf-8"))
        icons_data = {"icons": icons_json.get("icons", [])}

    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    env.globals.update({
        "repo_url": "https://github.com/Edinburgh-Genome-Foundry/SBOL-Visual-CSS",
        **icons_data
    })
    page_templates = sorted(
        template_path
        for template_path in templates_dir.glob("*.html")
        if not template_path.name.startswith("_")
    )

    for template_path in page_templates:
        template = env.get_template(template_path.name)
        output_path = dist_dir / template_path.name
        output_path.write_text(template.render(), encoding="utf-8")
        print(f"Rendered {output_path.relative_to(repo_root)}")


def build_docs() -> None:
    source_dir = Path(__file__).resolve().parent
    root = source_dir.parent
    dist_dir = root / "dist"
    assets_src = root / "assets"

    build_css_bundle()

    if assets_src.exists():
        shutil.copytree(assets_src, dist_dir / "assets", dirs_exist_ok=True)
        print(f"Synced assets to {dist_dir / 'assets'}")

    render_templates(root)


if __name__ == "__main__":
    build_docs()
