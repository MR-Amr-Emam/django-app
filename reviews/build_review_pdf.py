from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, BalancedColumns, PageBreak
from reportlab.graphics.shapes import Drawing, Line, Rect
from reportlab.lib.styles import ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from PIL import Image as PImage
from io import BytesIO

import os

PAGE_HEIGHT=defaultPageSize[1]
PAGE_WIDTH=defaultPageSize[0]


def pageTemplate(canvas, doc):
    canvas.drawString(inch, PAGE_HEIGHT - inch, "project review")
    canvas.line(0, PAGE_HEIGHT-inch*1.1, PAGE_WIDTH, PAGE_HEIGHT-inch*1.1)
    canvas.line(0, inch*0.7, PAGE_WIDTH, inch*0.7)
    canvas.drawString(inch, 0.5 * inch, "page number {}".format(doc.page))



def buildDoc(review_details ,comments, title, general_comment, BASE_DIR):
    path = os.path.join(os.path.join(BASE_DIR,"files/reviews"), title)
    doc = SimpleDocTemplate(path, pagesize=defaultPageSize)
    story = []


    if review_details.accepted == True:
        state = "Accepted"
        state_color = "#1D7E00"
    elif review_details.accepted == False:
        state = "Rejected"
        state_color = "#e02200"


    if general_comment.rate == "amazing":
        rate_text = "Amazing"
    elif general_comment.rate == "very-well":
        rate_text = "Very well"
    elif general_comment.rate == "good":
        rate_text = "Good"
    elif general_comment.rate == "weak":
        rate_text = "Weak"


    story.append(Spacer(0, 0.4*inch))
    story.append(Paragraph(state, ParagraphStyle("Helvetica",
    textColor=state_color, fontSize=40, leftIndent=0.2*PAGE_WIDTH)))

    line = Line(0,0, 4*inch, 0, strokeWidth=0.25, strokeColor="#c9c9c8")

    story.append(Spacer(0, 1.2*inch))
    story.append(Paragraph(review_details.review_date.strftime('%y-%m-%dT%H:%M'),
    ParagraphStyle("gg", fontSize=12, textColor="#1D7E00")))
    d = Drawing(0, 0.2*inch)
    d.add(line)
    story.append(d)


    story.append(Spacer(0, 0.2*inch))
    story.append(Paragraph("general rate: {}".format(rate_text),
    ParagraphStyle("gg", fontSize=12)))
    d = Drawing(0, 0.2*inch)
    d.add(line)
    story.append(d)


    story.append(Spacer(0, 0.2*inch))
    story.append(Paragraph("made by {}".format(review_details.project.publisher.username),
    ParagraphStyle("gg", fontSize=12)))
    d = Drawing(0, 0.2*inch)
    d.add(line)
    story.append(d)

    story.append(Spacer(0, 0.2*inch))
    story.append(Paragraph("reviewed by {}".format(review_details.reviewer.username),
    ParagraphStyle("gg", fontSize=12)))
    d = Drawing(0, 0.2*inch)
    d.add(line)
    story.append(d)

    story.append(Spacer(0, 0.5*inch))
    story.append(Paragraph(general_comment.comment, ParagraphStyle("gg", fontSize=16, leading=18, textColor="#171615")))

    story.append(PageBreak())

    for comment in comments:
        story.append(Spacer(0, 0.5 * inch))

        with PImage.open(comment.image_comment) as image_comment:
            height = image_comment.height * (PAGE_WIDTH * 0.8/image_comment.width)
            img_io = BytesIO()
            image_comment.save(img_io, "PNG")
            img_io.seek(0)
            img = Image(img_io, PAGE_WIDTH*0.8, height)
            story.append(img)

        if comment.rate == "amazing":
            rate_text = "Amazing!"
            rate_color = "#1D7E00"
        elif comment.rate == "very-well":
            rate_text = "Very well :)"
            rate_color = "#1D7E00"
        elif comment.rate == "good":
            rate_text = "Good :/"
            rate_color = "#e9bd0e"
        elif comment.rate == "weak":
            rate_text = "Weak :("
            rate_color = "#e02200"

        d = Drawing(0,0)
        d.add(Rect(-(1.1*inch - 0.1*PAGE_WIDTH), 0, PAGE_WIDTH*0.81, height, fillColor=None, strokeWidth=0.25))
        story.append(d)

        story.append(Spacer(0, 0.2*inch))
        comment_rate = Paragraph(rate_text, ParagraphStyle("gg", fontSize=25, textColor=rate_color))
        story.append(comment_rate)

        d = Drawing(0, 0.35*inch)
        d.add(Line(0,0,4*inch,0, strokeWidth=0.25))
        story.append(d)

        story.append(Spacer(0, 0.35*inch))
        comment_para = Paragraph(comment.comment, ParagraphStyle("gg", fontSize=15, leading=17, leftIndent=10, textColor="#171615"))
        story.append(comment_para)
        story.append(PageBreak())


    doc.build(story, onFirstPage=pageTemplate, onLaterPages=pageTemplate)



