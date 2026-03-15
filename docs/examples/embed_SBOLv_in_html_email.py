"""Embed SBOL-Visual-CSS elements in an HTML email.

To use SBOL-Visual-CSS in an HTML email it is sufficient to embed the full
content of `sbol-visual.css` in the HTML inside a `<style>` div.

This Python script shows a minimal example (don't forget to change the smtp
parameters so they match your account)
"""
import smtplib
import email

# LOAD THE WHOLE CSS CONTENT
visual_sbol_css_path = "../dist/sbol-visual-standalone.css"
with open(visual_sbol_css_path) as f:
    visual_sbol_css_content = f.read()

# CREATE AN HTML MESSAGE WITH EMBEDED CSS
message_html = """\
<html>
  <head>
      <style type="text/css"> %s </style>
  </head>
  <body>
    <p>Hi there!<br> Here is your construct: </p>
    <div class="sbol-visual">
        <div class="sbolv promoter"> P1 </div>
        <div class="sbolv ribosome-entry-site"> rbs 1 </div>
        <div class="sbolv cds"><em>acs</em></div>
        <div class="sbolv terminator"></div>
        <div class="sbolv insulator"></div>
    </div>
  </body>
</html>
""" % visual_sbol_css_content

# CREATE THE MESSAGE
msg = email.message.Message()
msg['Subject'] = 'Your DNA construct'
msg['From'] = "tintin.zulko@gmail.com"
msg['To'] = "my.recipient@gmail.com"
msg.add_header('Content-Type','text/html')
msg.set_payload(message_html)

# SEND THE MESSAGE
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()
smtp.login(user=msg['From'], password="sbolvisualcssrocks")
smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
