from __future__ import annotations

import shutil
from pathlib import Path

from build import build as build_css_bundle


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
    page_templates = sorted(
        template_path
        for template_path in templates_dir.glob("*.html")
        if not template_path.name.startswith("_")
    )

    for template_path in page_templates:
        template = env.get_template(template_path.name)
        output_path = docs_dir / template_path.name
        output_path.write_text(template.render(), encoding="utf-8")
        print(f"Rendered {output_path.relative_to(docs_dir.parent)}")


def build_docs() -> None:
    source_dir = Path(__file__).resolve().parent
    repo_dir = source_dir.parent
    docs_dir = repo_dir / "docs"
    docs_dist_dir = docs_dir / "dist"
    docs_css_path = docs_dist_dir / "sbol-visual-standalone.css"
    root_css_path = repo_dir / "dist" / "sbol-visual-standalone.css"
    examples_dir = repo_dir / "examples"
    docs_examples_dir = docs_dir / "examples"

    build_css_bundle()

    docs_dist_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root_css_path, docs_css_path)
    print(f"Synced {docs_css_path.relative_to(repo_dir)}")

    if examples_dir.exists():
        shutil.copytree(examples_dir, docs_examples_dir, dirs_exist_ok=True)
        print(f"Synced {docs_examples_dir.relative_to(repo_dir)}")

    render_templates(docs_dir)


if __name__ == "__main__":
    build_docs()
