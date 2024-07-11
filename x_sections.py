import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import tempfile
import os

@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

def plot_cross_section(df, id_line):
    subset = df[df['ID_LINE'] == id_line]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(subset['X'], subset['Z'], marker='o')
    ax.set_title(f'Cross Section ID_LINE {id_line}')
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.grid(True)
    plt.tight_layout()
    return fig

def export_to_pdf(df, id_lines):
    pdf = FPDF()
    temp_files = []
    for id_line in id_lines:
        fig = plot_cross_section(df, id_line)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_files.append(temp_file.name)
        fig.savefig(temp_file.name)
        pdf.add_page()
        pdf.image(temp_file.name, x=10, y=10, w=190)
        plt.close(fig)
    pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(pdf_output.name)
    for temp_file in temp_files:
        os.remove(temp_file)
    return pdf_output.name

st.title('Cross Section Visualizer')

uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        st.success('File uploaded successfully!')

        # Allow user to select ID_LINE values
        all_id_lines = df['ID_LINE'].unique().tolist()
        id_lines = st.multiselect('Select ID_LINE values to visualize', all_id_lines,
                                  default=all_id_lines[:min(5, len(all_id_lines))])

        if id_lines:
            for id_line in id_lines:
                st.pyplot(plot_cross_section(df, id_line))

            if st.button('Export Selected to PDF'):
                pdf_file = export_to_pdf(df, id_lines)
                with open(pdf_file, 'rb') as f:
                    st.download_button('Download PDF', f, file_name='cross_sections.pdf')
                os.remove(pdf_file)

        if st.button('Export All to PDF'):
            pdf_file = export_to_pdf(df, all_id_lines)
            with open(pdf_file, 'rb') as f:
                st.download_button('Download All PDF', f, file_name='all_cross_sections.pdf')
            os.remove(pdf_file)

    except Exception as e:
        st.error(f'Error processing file: {e}')
else:
    st.warning('Please upload a CSV file')