import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# python -m streamlit run main.py

data = pd.read_csv('Hl-2b Profiles.csv')


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

# Select ID Line
id_lines = data['ID_LINE'].unique()
selected_id_line = st.selectbox('Select Cross Section ID_LINE', id_lines)

# Plot the selected cross section
if selected_id_line is not None:
    plot = plot_cross_section(data, selected_id_line)
    st.pyplot(plot)

# Export to PDF
if st.button('Export All to PDF'):
    export_to_pdf(data, id_lines)
    st.success('PDF Exported Successfully!')