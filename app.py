import streamlit as st
from docx import Document
from io import BytesIO
import datetime

def create_treatment_sheet(data):
    doc = Document()
    doc.add_heading("Dr. Doodley Pet Hospital - Bangalore", 0)
    doc.add_paragraph(f"Pet Name: {data['pet_name']}       Pet ID: {data['pet_id']}")
    doc.add_paragraph(f"Date: {data['date']}       Time of Treatment: {data['time']}")
    doc.add_paragraph("")

    def add_section(title, cols, rows):
        doc.add_heading(title, level=1)
        table = doc.add_table(rows=1, cols=len(cols))
        for idx, col in enumerate(cols):
            table.rows[0].cells[idx].text = col
        for r in rows:
            row_cells = table.add_row().cells
            for idx, col in enumerate(cols):
                row_cells[idx].text = r.get(col.lower(), "")
        doc.add_paragraph("")

    add_section("Current Treatment Details",
                ["#", "Name", "Route", "ml", "Dose", "Remarks", "Billed"],
                [{k: v for k, v in zip(["#", "Name", "Route", "ml", "Dose", "Remarks", "Billed"], [str(i+1), d['name'], d['route'], d['ml'], d['dose'], d['remarks'], d['billed']])} for i, d in enumerate(data['injectables'])])

    add_section("Oral Medications",
                ["#", "Name", "Dose", "Remarks", "Billed"],
                [{k: v for k, v in zip(["#", "Name", "Dose", "Remarks", "Billed"], [str(i+1), d['name'], d['dose'], d['remarks'], d['billed']])} for i, d in enumerate(data['oral_meds'])])

    add_section("Food Details",
                ["Type of Food", "Quantity", "Remarks"],
                data['food'])

    add_section("Emergency Treatments",
                ["Name", "Dose", "Remarks", "Billed"],
                data['emergency'])

    doc.add_heading("General Notes / Observations", level=1)
    doc.add_paragraph(data['remarks'])
    doc.add_paragraph("")
    doc.add_paragraph(f"Temp: {data['temp']}    CRT: {data['crt']}    SpO2: {data['spo2']}    BP: {data['bp']}")
    doc.add_paragraph(f"Doctor: {data['doctor']}    Paravet: {data['paravet']}")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

st.title("IPD Treatment Sheet Generator")

with st.form("form"):
    st.subheader("Basic Info")
    pet_name = st.text_input("Pet Name")
    pet_id = st.text_input("Pet ID")
    date = st.date_input("Date", datetime.date.today())
    time = st.time_input("Time")

    def input_rows(prefix, labels, include_billed=False):
        arr = []
        for i in range(len(labels)):
            with st.expander(f"{prefix} #{i+1}"):
                row = {}
                for label in labels:
                    row[label.lower()] = st.text_input(label, key=f"{prefix.lower()}_{label}_{i}")
                if include_billed:
                    row["billed"] = st.selectbox("Billed", ["Yes", "No"], key=f"{prefix.lower()}_billed_{i}")
                arr.append(row)
        return arr

    injectables = input_rows("Injectable", ["Name", "Route", "ml", "Dose", "Remarks"], include_billed=True)
    oral_meds = input_rows("Oral Med", ["Name", "Dose", "Remarks"], include_billed=True)
    food = input_rows("Food", ["Type of Food", "Quantity", "Remarks"])
    emergency = input_rows("Emergency", ["Name", "Dose", "Remarks"], include_billed=True)

    st.subheader("Final Notes & Vitals")
    remarks = st.text_area("General Remarks")
    temp = st.text_input("Temperature")
    crt = st.text_input("CRT")
    spo2 = st.text_input("SpO2")
    bp = st.text_input("BP")
    doctor = st.text_input("Doctor")
    paravet = st.text_input("Paravet")

    submitted = st.form_submit_button("Generate & Download (.docx)")

if submitted:
    doc = create_treatment_sheet({
        'pet_name': pet_name,
        'pet_id': pet_id,
        'date': date,
        'time': time,
        'injectables': [r for r in injectables if r.get("name")],
        'oral_meds': [r for r in oral_meds if r.get("name")],
        'food': [r for r in food if r.get("type of food")],
        'emergency': [r for r in emergency if r.get("name")],
        'remarks': remarks,
        'temp': temp, 'crt': crt, 'spo2': spo2, 'bp': bp,
        'doctor': doctor, 'paravet': paravet
    })
    st.success("✅ Treatment sheet ready!")
    st.download_button(
        "Download as Word (.docx)",
        data=doc,
        file_name="Treatment_Sheet.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
