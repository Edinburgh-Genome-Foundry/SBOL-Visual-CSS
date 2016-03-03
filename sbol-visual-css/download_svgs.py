"""Script used to download and modify the SBOLV svgs.

This is a little helper script that was used to make visual-sbol-css.
It is not needed for the functioning of visual-sbol-css.
It works as follows:

- Download the zip of all SBOLV svgs from the official SBOL website.
- Unzip the svgs in SVG/
- For each svg add a very long horizontal line at the middle of the svg.
- For each SVG add a line in `visual-sbol.css` for the corresponding class.
"""

import os
import zipfile


zip_filename = "svgs.zip"
svg_folder_name = "SVG"
os.system("wget http://sbolstandard.org/?wpdmdl=425 -O " + zip_filename)

with open(zip_filename, 'rb') as f:
    z = zipfile.ZipFile(f)
    for name in z.namelist():
        if name.endswith(".svg"):
            z.extract(name, ".")


def replace_in_file(path, replace_dict):
    """Replace the file's content according to the replacement dictionary."""
    with open(path, "r") as f:
        text = f.read()
    for old, new in replace_dict.items():
        text = text.replace(old, new)
    with open(path, "w+") as f:
        f.write(text)

for name in sorted(os.listdir(svg_folder_name)):
    path = os.path.join(svg_folder_name, name)
    replace_in_file(path, {
        'viewBox="0 0 50 100"': 'viewBox="-200 0 450 100"',
        'width="50px"': 'width="450px"',
        '</defs>': '</defs><path d="M -200 50 L 250 50"/>\n'
    })

template = '.%s { background-image: url("%s/%s");}\n'
with open("visual-sbol.css", "a") as f:
    for name in os.listdir(svg_folder_name):
        f.write(template % (name[:-4], svg_folder_name, name))
