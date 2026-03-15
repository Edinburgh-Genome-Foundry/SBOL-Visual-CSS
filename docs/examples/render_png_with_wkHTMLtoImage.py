"""Render SBOL Visual elements to SVG using Python and wkHTMLtoImage.

This requires a recent version wkhtmltopdf/wkhtmltoimage installed.
Thids also requires PIL/Pillow installed.
"""

import os
import subprocess as sp
import tempfile
from PIL import Image
import PIL.ImageOps


def autocrop(filename, border_width=5):
    """Remove all white borders from a picture, then add a white border of
    size given by `border_width` (in pixels)"""
    image = Image.open(filename, mode="r").convert('L')
    inverted_image = PIL.ImageOps.invert(image)
    cropped = image.crop(inverted_image.getbbox())
    cropped_margin = PIL.ImageOps.expand(cropped, border_width, fill=255)
    cropped_margin.save(filename)


def render_sbolv(sbolv_elements, outfile, elements_zoom=1, width=600,
                 css_stylesheets=("sbol-visual-standalone.css",),
                 border_width=5):
    """Render a series of sbolv elements into an image file.

    Parameters
    ----------

    sbolv_elements
      A list of elements of the form (element_type, element_label)
      where element_type is "promoter", "cds", etc. and element_label is
      any text or HTML

    outfile
      Name or path of the output file. Valid extensions are .png, .jpeg, etc.

    elements_zoom
      Makes the elements and label appear bigger (zoom > 1) or smaller
      (zoom < 1)

    width
      Width in pixels of the final picture (not counting border)

    border_width
      Size in pixels of the white pixels border around the picture.
    """

    def get_content(fname):
        with open(fname) as f:
            content = f.read()
        return content

    css_content = "\n".join([
        '<style type="text/css"> %s </style>' % get_content(fname)
        for fname in css_stylesheets
    ])

    sbolv_elements_html = "\n".join([
        '<div class="sbolv %s">%s</div>' % (sbol_type, html_content)
        for sbol_type, html_content in sbolv_elements
    ])

    html = """
    <html>
      <head> %s </head>
      <body> <div class="sbol-visual"> %s </div> </body>
    </html>
    """ % (css_content, sbolv_elements_html)

    temp_html = tempfile.mkstemp(suffix=".html")[1]
    with open(temp_html, "w") as f:
        f.write(html)

    extension = os.path.splitext(outfile)[1][1:]
    process = sp.Popen(["wkhtmltoimage",
                        "--format", extension,
                        "--zoom", "%.1f" % elements_zoom,
                        "--width", "%d" % width,
                        "--disable-smart-width",
                        temp_html, outfile,
                        ],
                       stderr=sp.PIPE, stdout=sp.PIPE)
    out, err = process.communicate()
    print(err)
    os.remove(temp_html)
    autocrop(outfile, border_width=border_width)


# LET'S TRY IT !
if __name__ == "__main__":

    render_sbolv(
        sbolv_elements=[
            ("promoter", "P1"),
            ("cds", "my favourite gene with a super long name"),
            ("terminator", "Tr. 1"),
            ("promoter", "P2"),
            ("cds", "<em>acs</em>"),
            ("terminator", "Tr. 2")
        ],
        outfile="rendered_sbolv.png",
        css_stylesheets=["../dist/sbol-visual-standalone.css"]
    )
