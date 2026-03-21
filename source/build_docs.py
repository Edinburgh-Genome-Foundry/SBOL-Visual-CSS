"""Build the static docs website from templates."""

from __future__ import annotations
import json
import shutil
from pathlib import Path
from build_css import build as build_css_bundle

SOURCE_DIR = Path(__file__).resolve().parent
REPO_DIR = SOURCE_DIR.parent
TEMPLATES_DIR = REPO_DIR / "templates"
DIST_DIR = REPO_DIR / "dist"
ASSETS_SRC = REPO_DIR / "assets"
ICONS_JSON_PATH = DIST_DIR / "icons.json"
REPO_URL = "https://github.com/mtripnaux/SBOL-Visual-CSS"

def load_icons_data() -> dict:
    """Load icon metadata from the generated icons.json file."""
    icons_data = {}
    if ICONS_JSON_PATH.exists():
        icons_json = json.loads(ICONS_JSON_PATH.read_text(encoding="utf-8"))
        icons_data = {
            "icons": icons_json.get("icons", []),
            "icons_count": icons_json.get("count", 0)
        }
    return icons_data


def render_templates() -> None:
    """Render all Jinja2 templates from the templates directory."""
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError as exc:
        raise RuntimeError(
            "jinja2 is required to build the documentation. Install it with 'pip install jinja2'."
        ) from exc

    if not TEMPLATES_DIR.exists():
        raise FileNotFoundError(f"Templates directory not found: {TEMPLATES_DIR}")

    icons_data = load_icons_data()

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    env.globals.update({
        "repo_url": REPO_URL,
        **icons_data
    })
    
    # non-partial
    page_templates = sorted(
        template_path
        for template_path in TEMPLATES_DIR.glob("*.html")
        if not template_path.name.startswith("_")
    )

    # Render every templates
    for template_path in page_templates:
        template = env.get_template(template_path.name)
        output_path = DIST_DIR / template_path.name
        output_path.write_text(template.render(), encoding="utf-8")
        print(f"Rendered {output_path.relative_to(REPO_DIR)}")


def sync_assets() -> None:
    """Sync assets directory to the distribution folder."""
    if ASSETS_SRC.exists():
        shutil.copytree(ASSETS_SRC, DIST_DIR / "assets", dirs_exist_ok=True)
        print(f"Synced assets to {DIST_DIR / 'assets'}")


def build_docs() -> None:
    """Build the complete documentation site."""
    build_css_bundle()
    
    # Sync assets and render templates
    sync_assets()
    render_templates()


if __name__ == "__main__":
    build_docs()
