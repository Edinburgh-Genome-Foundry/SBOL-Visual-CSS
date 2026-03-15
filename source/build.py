from __future__ import annotations

import base64
import json
from datetime import datetime, timezone
from pathlib import Path


def to_label(name: str) -> str:
    return name.replace("-", " ").title()


def svg_to_data_uri(svg_path: Path) -> str:
    svg_bytes = svg_path.read_bytes()
    encoded = base64.b64encode(svg_bytes).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def build_css(base_css: str, icons: list[dict[str, str]]) -> str:
    icon_map = {icon["name"]: icon for icon in icons}
    default_icon = icon_map.get("user-defined")

    if default_icon is not None:
        base_css = base_css.replace(
            'background-image: url("SVG/user-defined.svg");',
            f'background-image: url("{default_icon["dataUri"]}");',
        )

    generated_lines = [
        "",
        "/* Generated from icons.json by build.py */",
    ]
    generated_lines.extend(
        f'.sbolv.{icon["name"]} {{ background-image: url("{icon["dataUri"]}");}}'
        for icon in icons
    )
    return base_css.rstrip() + "\n" + "\n".join(generated_lines) + "\n"


def build() -> None:
    source_dir = Path(__file__).resolve().parent
    repo_dir = source_dir.parent
    svg_dir = source_dir / "SVG"
    base_css_path = source_dir / "base.css"
    icons_json_path = source_dir / "icons.json"
    root_dist_dir = repo_dir / "dist"
    root_css_path = root_dist_dir / "sbol-visual-standalone.css"

    svg_paths = sorted(svg_dir.glob("*.svg"))
    icons = []

    for svg_path in svg_paths:
        name = svg_path.stem
        data_uri = svg_to_data_uri(svg_path)
        icons.append(
            {
                "name": name,
                "className": f"sbolv {name}",
                "file": str(svg_path.relative_to(source_dir)).replace("\\", "/"),
                "label": to_label(name),
                "dataUri": data_uri,
            }
        )

    icons_payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "count": len(icons),
        "icons": icons,
    }
    icons_json_path.write_text(
        json.dumps(icons_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    base_css = base_css_path.read_text(encoding="utf-8").rstrip()
    generated_icons = json.loads(icons_json_path.read_text(encoding="utf-8"))["icons"]
    target_css_content = build_css(base_css=base_css, icons=generated_icons)

    root_dist_dir.mkdir(parents=True, exist_ok=True)
    root_css_path.write_text(target_css_content, encoding="utf-8")

    print(f"Generated {icons_json_path} with {len(icons)} icons")
    print(f"Published {root_css_path}")


if __name__ == "__main__":
    build()
