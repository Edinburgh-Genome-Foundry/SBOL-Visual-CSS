import os
import base64

with open("sbol-visual.css", "r") as f:
    css = f.read()

for name in os.listdir("SVG"):
    with open(os.path.join("SVG", name), "r") as f:
        svg_content = " ".join(f.read().splitlines()[2:])
    svg_content = base64.b64encode(svg_content.encode('utf-8'))
    css = css.replace('"SVG/%s"' % name,
                      '"data:image/svg+xml;base64,%s"' % svg_content)
target = os.path.join("..", "dist", "sbol-visual-standalone.css")

with open(target, "w+") as f:
    f.write(css)
