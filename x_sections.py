import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF


# Function to plot cros ssection
def plot_cross_section(df, id_line):
    subset = df[df['ID_LINE'] == id_line]
    plt.figure(figsize=(10, 6))
    plt.plot(subset['X'], subset['Z'], marker='o')
    plt.title(f'Cross Section ID_LINE {id_line}')
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.grid(True)
    plt.tight_layout()
    return plt


# Function to export plots to PDF
def export_to_pdf(df, id_lines):
    pdf = FPDF()
    for id_line in id_lines:
        plot = plot_cross_section(df, id_line)
        plot.savefig(f'temp_plot_{id_line}.png')
        pdf.add_page()
        pdf.image(f'temp_plot_{id_line}.png', x=10, y=10, w=190)
        plot.close()
    pdf.output('cross_sections.pdf')


st.title('Cross Section Visualizer')
st.title('Upload CSV file')
uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning('Please upload a CSV file')
