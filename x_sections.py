import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF


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
