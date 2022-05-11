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

def myPageWrapper2(patient_data, specimen_details):
    # template for static, non-flowables, on the first page
    # draws all of the contact information at the top of the page
    def myPage(canvas, doc):
        canvas.saveState()  # save the current state
        # patient data column
        canvas.drawString(
            patient_data_placement,
            HEIGHT - (.4 * inch),
            "Patient Information" )
        canvas.drawString(
            patient_data_placement,
            HEIGHT - (.6 * inch),
            #"Name: %s, %s"%(patient_data['name']['last'],patient_data['name']['first']) )
            "Patient ID: %s"%patient_data['ID'] )
        canvas.drawString(
            patient_data_placement,
            HEIGHT - (.8 * inch),
            "DOB: %s"%patient_data['DOB'])  
        canvas.drawString(
            patient_data_placement,
            HEIGHT - (1.0 * inch),
            "Sex: %s"%patient_data['SEX'])
        canvas.drawString(
			patient_data_placement,
			HEIGHT - (1.2 * inch),
			"ACC #: %s"%patient_data['ACC'])
        # test data column
        canvas.drawString(
            specimen_details_placement,
            HEIGHT - (.4 * inch),
            "Specimen Details" )
        canvas.drawString(
            specimen_details_placement,
            HEIGHT - (.6 * inch),
            "Received Date: %s"%specimen_details['date_received'] )
        canvas.drawString(
            specimen_details_placement,
            HEIGHT - (.8 * inch),
            "Report Date: %s"%specimen_details['date_report'])  
        canvas.drawString(
            specimen_details_placement,
            HEIGHT - (1.0 * inch),
            "Test Type: %s"%specimen_details['test_type'])
        canvas.drawCentredString(
			WIDTH / 2.0,
			HEIGHT - (1.6 * inch),
			"Clinical Genetic Report")
        canvas.line(.4 * inch, HEIGHT - 1.8*inch, 
            WIDTH - (.4 * inch), HEIGHT - 1.8*inch)
        # restore the state to what it was when saved
        canvas.restoreState()
    return myPage

st.write(
    """This application allows lab personel to select appropriate language from pharmacogenetic sources
    and generates a report for the ordering physician"""
)

#st.button("Import patient lab results")
uploaded_file = st.file_uploader("Import patient lab results")
patient_data = {}


patient_data = {'name': {'first':'Janae', 'last': 'Spencer'}, 
                'DOB':'07/04/1990', 
                'SEX': 'Female',
                'ACC': 'A001237-5-05'}
specimen_details = {'date_received':'04/01/2022',
                    'date_report': '05/01/2022',
                    'test_type': 'AOA'}

if uploaded_file is not None:  
    with open(uploaded_file.name) as json_file:
        lab_results = json.load(json_file)
    #lab_results = json.load(uploaded_file.name)
    patient_data["ID"] = lab_results['PATIENT']['id']
    patient_data["DOB"] = lab_results['PATIENT']['birthDate']
  
    
    #st.write("comparing patient variant data to available pharmogenetic data...")
    if "pdata_loaded" not in st.session_state:
        my_bar = st.progress(0)
        status_text = st.empty()
        for percent_complete in range(100):
             time.sleep(0.1)
             my_bar.progress(percent_complete + 1)
             status_text.text("comparing patient variant data to available pharmogenetic data...")
        status_text = st.empty()
        st.success("Patient data processing complete")
        st.session_state["pdata_loaded"] = True















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
