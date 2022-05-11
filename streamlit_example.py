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

#if uploaded_file:
#    df = pd.read_csv(uploaded_file)

if uploaded_file: #is not None:  
    #with open(uploaded_file.name) as json_file:
    #    lab_results = json.load(json_file)
    #lab_results = json.load( open(uploaded_file.name) )
    #lab_results = json.load(uploaded_file.name)
    lab_results = pd.read_json(uploaded_file)
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

#pgx = pd.read_csv('pgkb_cpic.txt',sep='\t')
uploaded_file = st.file_uploader("Import PharmGen data")
if uploaded_file is not None:  
    #with open(uploaded_file.name) as tsv_file:
    #    pgx = pd.read_csv(tsv_file,sep='\t')
    pgx = pd.read_csv(uploaded_file,sep='\t')
#pgx = pd.read_csv('PharmGenResults1.txt',sep='\t')
variants = []
medicines = []
for idx,row in pgx.iterrows():
# =============================================================================
#     if row["pgkb_GenotypeAllele"] not in variants:
#         variants.append( row["pgkb_GenotypeAllele"] )
#     if row["pgkb_chemicals"] not in medicines:
#         medicines.append( row["pgkb_chemicals"] )
# =============================================================================
    if row["GenotypeAllele"] not in variants:
        variants.append( row["GenotypeAllele"] )
    if row["chemicals"] not in medicines:
        medicines.append( row["chemicals"] )
    variants = [x for x in variants if type(x)==type('') or not math.isnan(x)]
    medicines = [x for x in medicines if type(x)==type('') or not math.isnan(x)]

#st.write(variants)
#st.write(medicines)



left, right = st.columns(2)

right.write("SUMMARY")


#right.image("template.png", width=300)

#env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
#template = env.get_template("template.html")

def clear(option):
    if option in st.session_state:
        del st.session_state[option]

#meds = {}
#meds["CURRENT"] = ["Metoprolol, Ondansetron, Strattera","Trimipramine (Surmontil®)"]
#meds["POTENTIAL"] =  ["Atomoxetine (Strattera®)","Succinylcholine (Anectine®, Quelicin®)"]
#
#language = {"Metoprolol, Ondansetron, Strattera":{"FDA":"blah blah "*9,"CPIC":"blah blah "*9,"PharmGKB":"blah blah "*9},
#            "Atomoxetine (Strattera®)":{"FDA":"blah blah "*9,"CPIC":"blah blah "*9,"PharmGKB":"blah blah "*9},
#            "Succinylcholine (Anectine®, Quelicin®)":{"FDA":"blah blah "*9,"CPIC":"blah blah "*9,"PharmGKB":"blah blah "*9},
#            "Trimipramine (Surmontil®)":{"FDA":"blah blah "*9,"CPIC":"blah blah "*9,"PharmGKB":"blah blah "*9},
#            }

summary_text = ''

# =============================================================================
# left.write("Fill in the data:")
# form = left.form("template_form")
# 
# student = form.text_input("Student name")
# course = form.selectbox(
#     "Choose course",
#     ["Report Generation in Streamlit", "Advanced Cryptography"],
#     index=0,
# )
# grade = form.slider("Grade", 1, 100, 60)
# =============================================================================

variant_choice = left.radio("Select gene variant to work on:",
                     variants)
left.write("You selected: %s"%variant_choice)

#variant_relevant_rows = pgx[pgx["pgkb_GenotypeAllele"]==variant_choice]
variant_relevant_rows = pgx[pgx["GenotypeAllele"]==variant_choice]

#for m in medicines:
    #r = variant_relevant_rows[variant_relevant_rows["pgkb_chemicals"]==m]
#med_options = pd.Series(variant_relevant_rows["pgkb_chemicals"]).unique()
med_options = pd.Series(variant_relevant_rows["chemicals"]).unique()
med_choice = left.radio("Select medicine:",
                     med_options)
left.write("You selected: %s"%med_choice)

#relevant_rows = variant_relevant_rows[variant_relevant_rows["pgkb_chemicals"]==med_choice]
relevant_rows = variant_relevant_rows[variant_relevant_rows["chemicals"]==med_choice]

cpic = relevant_rows.loc[:,[col for col in relevant_rows.columns if 'cpic' in col]]
pgkb = relevant_rows.loc[:,[col for col in relevant_rows.columns if 'cpic' not in col]]

lang_options = []
for idx,row in cpic.iterrows():
    text_block = '\n'.join( [str(c) for c in row if type(c)==type('') or not math.isnan(c)] )
    lang_options.append( "CPIC: %s"%text_block )
for idx,row in pgkb.iterrows():
    text_block = '\n'.join( [str(c) for c in row if type(c)==type('') or not math.isnan(c)] )
    lang_options.append( "PGKB: %s"%text_block )
#st.write(lang_options)

#lang_options = ["%s: %s"%(k,language[option][k]) for k in language[option].keys() ]
lang_options.append("CUSTOM TEXT BLOCK")
lang_options.append("CLEAR ------")
lang_choice = left.radio("What language do you want to report",
     lang_options )
if lang_choice == "CUSTOM TEXT BLOCK":
    lang_choice = left.text_input('Compose text and press [enter] to submit to form', 'CUSTOM: ')
#st.write(pgkb)

# =============================================================================
# med_cat = left.radio("Select medication set to work on:",
#                    ("CURRENT MEDICATIONS", "POTENTIAL MEDICATIONS") )
# 
# left.write(med_cat)
# option = left.radio("Select language for ", 
#           (m for m in meds[med_cat.split()[0]]) )
# =============================================================================

    
#option = st.selectbox(
#     'select among current meds',
#     [m for m in med_current])

#summary += option

#print( option)
# =============================================================================
# left.write("You selected: %s"%option)
# #left.write('You selected:', option)
# lang_options = ["%s: %s"%(k,language[option][k]) for k in language[option].keys() ]
# lang_options.append("CUSTOM TEXT BLOCK")
# lang_options.append("CLEAR ------")
# lang_choice = left.radio("What language do you want to report",
#      lang_options )
# if lang_choice == "CUSTOM TEXT BLOCK":
#     lang_choice = left.text_input('Movie title', 'CUSTOM: ')
# =============================================================================
    
# =============================================================================
# if left.button('STORE CHOICE'):
#     #if 'key' not in st.session_state:
#     if lang_choice == "CLEAR ------":
#         #st.session_state[option] = {"source": '', "lang": ''} 
#         clear(option)
#     else:
#         lang_choice = lang_choice.split(": ")
#         st.session_state[option] = {"source": lang_choice[0],"lang": lang_choice[1]}
# =============================================================================
        
if left.button('STORE CHOICE'):
    #if 'key' not in st.session_state:
    if lang_choice == "CLEAR ------":
        #st.session_state[option] = {"source": '', "lang": ''} 
        clear(med_choice)
    else:
        lang_choice = lang_choice.split(": ")
        st.session_state[(med_choice,variant_choice)] = {"source": lang_choice[0],"lang": lang_choice[1]}
    
#submit = form.form_submit_button("Generate PDF")
# =============================================================================
# if right.button("CLEAR CURRENT"):
#     for m in meds["CURRENT"]:
#         clear(m)
# 
# if right.button("CLEAR POTENTIAL"):
#     for m in meds["POTENTIAL"]:
#         clear(m)
# 
# if right.button("CLEAR ALL"):
#     summary_text = ''
#     for c in ["CURRENT","POTENTIAL"]:
#         for m in meds[c]:
#             clear(m)
# 
# =============================================================================
#for c in ["CURRENT","POTENTIAL"]:
# =============================================================================
# for c in ["CURRENT","POTENTIAL"]:
#     summary_text += c + " MEDICATIONS\n\n"
#     for m in medicines[c]:
#         if m in st.session_state:
#             summary_text += "%s: %s (SOURCE: %s)"%(m, st.session_state[m]["lang"], st.session_state[m]["source"]) + "\n\n"
# =============================================================================
for m in medicines:
    summary_text += m.upper() + "\n\n"
    for v in variants:
        if (m,v) in st.session_state:
            summary_text += v.upper() + "\n\n"
            summary_text += "%s: %s (SOURCE: %s)"%(m, st.session_state[(m,v)]["lang"], st.session_state[(m,v)]["source"]) + "\n\n\n"

#right.write("=== SUMMARY ===")
right.write(summary_text)

if right.button("DISPLAY REPORT"):
    generate_print_pdf(summary_text,patient_data, specimen_details)
   # with open("dummy.pdf", "rb") as pdf_file:
   #     PDFbyte = pdf_file.read()
    with open("dummy.pdf", "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
    #pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<embed src="https://d30b7srod7pe7m.cloudfront.net/uploads/2020/08/Figure_Managing-acute-asthma-in-adults_web.pdf" width="700" height="1000" type="application/pdf">'
    st.write(pdf_display)

    # Displaying File
    right.markdown(pdf_display, unsafe_allow_html=True)
    #right.markdown("# Hello!", unsafe_allow_html=True)



#def hello(c):
#    c.drawString(100,100,"Hello World")
#c = canvas.Canvas("hello.pdf")
#hello(c)
#c.showPage()
#c.save()

#st.title('Uber pickups in NYC')

#DATE_COLUMN = 'date/time'
#DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

#@st.cache
#def load_data(nrows):
#    data = pd.read_csv(DATA_URL, nrows=nrows)
#    lowercase = lambda x: str(x).lower()
#    data.rename(lowercase, axis='columns', inplace=True)
#    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
#    return data

#data_load_state = st.text('Loading data...')
#data = load_data(10000)
#data_load_state.text("Done! (using st.cache)")

#if st.checkbox('Show raw data'):
#    st.subheader('Raw data')
#    st.write(data)

#st.subheader('Number of pickups by hour')
#hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
#st.bar_chart(hist_values)

# Some number in the range 0-23
#hour_to_filter = st.slider('hour', 0, 23, 17)
#filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

#st.subheader('Map of all pickups at %s:00' % hour_to_filter)
#st.map(filtered_data)







st.write(st.session_state)
