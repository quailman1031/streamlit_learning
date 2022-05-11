import streamlit as st
import pandas as pd
import numpy as np
from reportlab.pdfgen import canvas


from datetime import date
import streamlit as st
from streamlit.components.v1 import iframe
from os.path import exists
from os import remove

import base64
#import pandas as pd
import json
#import StringIO
import time
import pandas as pd

import math

from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfdoc
from reportlab.pdfbase.pdfmetrics import registerFont, registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_RIGHT

# Set the page height and width
HEIGHT = 11 * inch
WIDTH = 8.5 * inch



patient_data_placement = WIDTH/2.0 - 1.0*inch
specimen_details_placement = patient_data_placement + 3.0*inch

# Set our styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Content',
                          #fontFamily='Inconsolata',
                          fontSize=8,
                          spaceAfter=.1*inch))

def generate_print_pdf(data, patient_data, specimen_details):
    #if exists("dummy.pdf"):
    #    remove("dummy.pdf")
    pdfname = 'dummy.pdf'
    doc = SimpleDocTemplate(
        pdfname,
        pagesize=letter,
        bottomMargin=.5 * inch,
        topMargin=2.0 * inch,
        rightMargin=.4 * inch,
        leftMargin=.4 * inch)  # set the doc template
    style = styles["Normal"]  # set the style to normal
    elements = []  # create a blank elements
# =============================================================================
#     contentTable = Table(
#         data,
#         colWidths=[
#             0.8 * inch,
#             6.9 * inch])
#     tblStyle = TableStyle([
#         ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
#         #('FONT', (0, 0), (-1, -1), 'Inconsolata'),
#         ('FONTSIZE', (0, 0), (-1, -1), 8),
#         ('VALIGN', (0, 0), (-1, -1), 'TOP'),
#         ('ALIGN', (0, 0), (-1, -1), 'LEFT')])
#     contentTable.setStyle(tblStyle)
#     elements.append(contentTable)
    #elements.append(Table(data.split('\n')))
    for p in data.split('\n'):
        elements.append(Paragraph(p, styles["Normal"]))
# =============================================================================
    
# =============================================================================
#     data= [["CATEGORY", "DRUG CLASS", "STANDARD PRECAUTIONS", "USE WITH CAUTION", 'CONSIDER ALTERNATIVES'],
#     [' ', 'Anti-ADHD Agents', ' ', 'Atomoxetine (Strattera®)', ' '],
#     ['20', '21', '22', '23', '24'],
#     ['30', '31', '32', '33', '34']]
#     
#     t=Table(data,5*[0.4*inch], 4*[0.4*inch])
#     
#     t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
#     ('TEXTCOLOR',(1,1),(-2,-2),colors.red),
#     ('VALIGN',(0,0),(0,-1),'TOP'),
#     ('TEXTCOLOR',(0,0),(0,-1),colors.blue),
#     ('ALIGN',(0,-1),(-1,-1),'CENTER'),
#     ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
#     ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
#     ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
#     ('BOX', (0,0), (-1,-1), 0.25, colors.black),
#     ]))
#             elements.append(t)
# =============================================================================
    

    
    doc.build(
        elements,
        #onFirstPage=myPageWrapper(contact)
        onFirstPage=myPageWrapper2(patient_data,specimen_details)
        )
    return pdfname





















def hello(c):
    c.drawString(100,100,"Hello World")
c = canvas.Canvas("hello.pdf")
hello(c)
c.showPage()
c.save()

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)
