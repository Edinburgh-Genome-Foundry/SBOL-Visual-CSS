"""Build the standalone CSS bundle from SVGs and base CSS."""

from __future__ import annotations
import base64
import json
from datetime import datetime, timezone
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parent
REPO_DIR = SOURCE_DIR.parent
SVG_DIR = SOURCE_DIR / "SVG"
BASE_CSS_PATH = SOURCE_DIR / "base.css"
DIST_DIR = REPO_DIR / "dist"
ICONS_JSON_PATH = DIST_DIR / "icons.json"
CSS_OUTPUT_PATH = DIST_DIR / "sbol-visual-standalone.css"

def to_label(name: str) -> str:
    """Converts kebab-case to Title Case."""
    return name.replace("-", " ").title()


def svg_to_data_uri(svg_path: Path) -> str:
    """Convert SVG from path to base64 URI."""
    svg_bytes = svg_path.read_bytes()
    encoded = base64.b64encode(svg_bytes).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def replace_in_text(text: str, replace_dict: dict[str, str]) -> str:
    """Replaces strings in text using a dictionary."""
    for old, new in replace_dict.items():
        text = text.replace(old, new)
    return text


def build_css(base_css: str, icons: list[dict[str, str]]) -> str:
    """Build the standalone CSS library"""
    icon_map = {icon["name"]: icon for icon in icons}
    default_icon = icon_map.get("user-defined")

    replacements = {}
    if default_icon is not None:
        replacements['background-image: url("SVG/user-defined.svg");'] = (
            f'background-image: url("{default_icon["dataUri"]}");'
        )
    
    base_css = replace_in_text(base_css, replacements)

    generated_lines = [
        "",
        "/* Generated from icons.json by build_css.py */",
    ]
    generated_lines.extend(
        f'.sbolv.{icon["name"]} {{ background-image: url("{icon["dataUri"]}");}}'
        for icon in icons
    )
    return base_css.rstrip() + "\n" + "\n".join(generated_lines) + "\n"


def collect_icons() -> list[dict[str, str]]:
    """Collect and process all SVGs icons from /source."""
    svg_paths = sorted(SVG_DIR.glob("*.svg"))
    icons = []

    for svg_path in svg_paths:
        name = svg_path.stem
        data_uri = svg_to_data_uri(svg_path)
        icons.append(
            {
                "name": name,
                "className": f"sbolv {name}",
                "file": str(svg_path.relative_to(SOURCE_DIR)).replace("\\", "/"),
                "label": to_label(name),
                "dataUri": data_uri,
            }
        )
    
    return icons


def build() -> None:
    """Build the CSS bundle and icons metadata"""
    icons = collect_icons()

    icons_payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "count": len(icons),
        "icons": icons,
    }
    
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    
    ICONS_JSON_PATH.write_text(
        json.dumps(icons_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    base_css = BASE_CSS_PATH.read_text(encoding="utf-8").rstrip()
    generated_icons = json.loads(ICONS_JSON_PATH.read_text(encoding="utf-8"))["icons"]
    css_content = build_css(base_css=base_css, icons=generated_icons)

    CSS_OUTPUT_PATH.write_text(css_content, encoding="utf-8")

    print(f"Generated {ICONS_JSON_PATH} with {len(icons)} icons")
    print(f"Published {CSS_OUTPUT_PATH}")


if __name__ == "__main__":
    build()
