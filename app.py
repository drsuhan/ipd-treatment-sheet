# IPD Case Sheet Generator Web Interface for Dr. Doodley Pet Hospital

import datetime
import streamlit as st
from docx import Document
from io import BytesIO

injectable_options = sorted([
    "ADRENALINE", "Althromb", "AMIKACIN", "AMOXY+SULBACTUM", "AMOXYCLAV", "APOMORPHINE", "ATROPINE",
    "BOTROPASE", "BUPRENORPHINE", "BUTORPHANOL", "CALCIUM GLUCONATE", "CARPROFEN", "CEFTRIAXONE", "CEFTIOFUR",
    "CONVENIA", "CPM", "DARBOPOIETIN", "D5", "D25", "DERIPHYLIN", "DEXAMETHASONE", "DEXMEDETOMIDINE", "DIAZEPAM",
    "DICYCLOMINE", "DIGYTON", "DNS", "DOXOPRAM", "Doxycycline", "EMEPET", "ERYTHROPOEITIN", "ETAMSYLATE",
    "FERRITAS", "FILGASTRIM", "FRUSEMIDE", "FPP", "GENTAMICIN", "GLYCOPYRROLATE", "HEPTOMAC", "IMIDOCARB",
    "INSULIN", "IVERMOCTIN", "KETAMINE", "LECETRACETEM", "LIGNOCAINE", "MANITOL", "MAROPITANT", "MELOXICAM",
    "MEROPENEM", "MIDAZOLAM", "NAC", "NS", "ONDENSETRON", "PANTAPRAZOLE", "PERINORM", "PREDNISOLONE",
    "PROPOFOL", "RANTAC", "RL", "SOLUMEDROL", "STEMETIL", "THIOSOL", "TRENAXEMIC ACID", "TRIBIVET", "VETALOG",
    "VINCRISTICINE", "XYLAZINE"
])

oral_medications = sorted([
    # your long list of oral medications here (truncated for brevity)
])

def generate_ipd_case_sheet_docx(data):
    doc = Document()
    doc.add_heading('Dr. Doodley Pet Hospital - Bangalore', 0)

    doc.add_paragraph(f"Pet Name: {data['pet_name']}     Pet ID: {data['pet_id']}")
    doc.add_paragraph(f"Date: {data['date']}     Time of Treatment: {data['time']}")

    doc.add_heading("Current Treatment Details", level=2)
    table = doc.add_table(rows=1, cols=7)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '#'
    hdr_cells[1].text = 'Name'
    hdr_cells[2].text = 'Route'
    hdr_cells[3].text = 'ml'
    hdr_cells[4].text = 'Dose'
    hdr_cells[5].text = 'Remarks'
    hdr_cells[6].text = 'Billed'
    for i, item in enumerate(data['injectables'], 1):
        row = table.add_row().cells
        row[0].text = str(i)
        row[1].text = item['name']
        row[2].text = item['route']
        row[3].text = item['ml']
        row[4].text = item['dose']
        row[5].text = item['remarks']
        row[6].text = item['billed']

    doc.add_heading("Oral Medications", level=2)
    table = doc.add_table(rows=1, cols=5)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '#'
    hdr_cells[1].text = 'Name'
    hdr_cells[2].text = 'Dose'
    hdr_cells[3].text = 'Remarks'
    hdr_cells[4].text = 'Billed'
    for i, item in enumerate(data['orals'], 1):
        row = table.add_row().cells
        row[0].text = str(i)
        row[1].text = item['name']
        row[2].text = item['dose']
        row[3].text = item['remarks']
        row[4].text = item['billed']

    doc.add_heading("Food Details", level=2)
    doc.add_paragraph(f"{data['food_type']} - {data['food_qty']}")
    if data['food_type'] == "Other" and data['food_other']:
        doc.add_paragraph(f"Other Food Details: {data['food_other']}")

    doc.add_heading("Emergency / Remarks", level=2)
    doc.add_paragraph(data['remarks'])

    doc.add_paragraph(f"\nTemp: {data['temp']}     CRT: {data['crt']}     Spo2: {data['spo2']}     BP: {data['bp']}")
    doc.add_paragraph(f"Doctor: {data['doctor']}     Paravet: {data['paravet']}")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

st.title("IPD Treatment Sheet Generator - Dr. Doodley Pet Hospital")

st.subheader("Oral Medications")
orals = []
num_orals = st.number_input("Number of Oral Medications", min_value=0, max_value=15, value=0, step=1)
for i in range(num_orals):
    with st.expander(f"Oral Medication {i+1}"):
        name = st.selectbox(f"Name {i+1}", options=[""] + oral_medications, key=f"oral_name_{i}")
        dose = st.text_input(f"Dose {i+1}", key=f"oral_dose_{i}")
        remarks = st.text_input(f"Remarks {i+1}", key=f"oral_remarks_{i}")
        billed = st.text_input(f"Billed {i+1}", key=f"oral_billed_{i}")
        orals.append({"name": name, "dose": dose, "remarks": remarks, "billed": billed})
