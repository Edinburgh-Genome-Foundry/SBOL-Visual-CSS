from __future__ import annotations

import shutil
from pathlib import Path

from build_css import build as build_css_bundle


def render_templates(docs_dir: Path) -> None:
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError as exc:
        raise RuntimeError(
            "jinja2 is required to build the documentation. Install it with 'pip install jinja2'."
        ) from exc

    templates_dir = docs_dir / "templates"
    if not templates_dir.exists():
        raise FileNotFoundError(f"Templates directory not found: {templates_dir}")

    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    env.globals.update({
        "repo_url": "https://github.com/mtripnaux/SBOL-Visual-CSS"
    })
    page_templates = sorted(
        template_path
        for template_path in templates_dir.glob("*.html")
        if not template_path.name.startswith("_")
    )

    for template_path in page_templates:
        template = env.get_template(template_path.name)
        output_path = docs_dir / "dist" / template_path.name
        output_path.write_text(template.render(), encoding="utf-8")
        print(f"Rendered {output_path.relative_to(docs_dir.parent)}")


def build_docs() -> None:
    source_dir = Path(__file__).resolve().parent
    root = source_dir.parent
    docs = root / "docs"
    docs_dist_dir = docs / "dist"
    
    root_dist_dir = root / "dist"
    docs_assets = docs / "assets"
    
    examples_dir = root / "examples"
    docs_examples_dir = docs / "examples"

    build_css_bundle()

    if root_dist_dir.exists():
        shutil.copytree(root_dist_dir, docs_dist_dir, dirs_exist_ok=True)
        print(f"Synced {docs_dist_dir.relative_to(root)} from {root_dist_dir.relative_to(root)}")

    if docs_assets.exists():
        docs_assets_target = docs_dist_dir / "assets"
        shutil.copytree(docs_assets, docs_assets_target, dirs_exist_ok=True)
        print(f"Synced {docs_assets.relative_to(root)} from {docs_assets.relative_to(root)}")

    # if examples_dir.exists():
    #     shutil.copytree(examples_dir, docs_examples_dir, dirs_exist_ok=True)
    #     print(f"Synced {docs_examples_dir.relative_to(repo_dir)}")

    render_templates(docs)


if __name__ == "__main__":
    build_docs()
