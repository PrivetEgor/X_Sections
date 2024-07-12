import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os
import zipfile
import io


@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)


def plot_cross_section(df, id_line):
    subset = df[df['KP'] == id_line]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(subset['X'], subset['Z'], marker='o')
    ax.set_title(f'Cross Section KP {id_line}')
    ax.set_xlabel('X')
    ax.set_ylabel('Z')
    ax.grid(True)
    plt.tight_layout()
    return fig


def export_to_png(df, id_lines):
    png_files = []
    for id_line in id_lines:
        fig = plot_cross_section(df, id_line)
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        png_files.append((f'cross_section_{id_line}.png', img_buffer.getvalue()))
        plt.close(fig)
    return png_files


st.title('Cross Section Visualizer📈')

uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
        st.success('File uploaded successfully!')

        # Allow user to select ID_LINE values
        all_id_lines = df['KP'].unique().tolist()
        id_lines = st.multiselect('Select ID_LINE values to visualize', all_id_lines,
                                  default=all_id_lines[:min(5, len(all_id_lines))])

        if id_lines:
            for id_line in id_lines:
                st.pyplot(plot_cross_section(df, id_line))

            if st.button('Export Selected as PNG'):
                png_files = export_to_png(df, id_lines)

                # Create a zip file containing all PNG images
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for filename, file_content in png_files:
                        zip_file.writestr(filename, file_content)

                # Offer the zip file for download
                st.download_button('Download Selected PNGs', zip_buffer.getvalue(), file_name='cross_sections.zip',
                                   mime='application/zip')

        if st.button('Export All as PNG'):
            png_files = export_to_png(df, all_id_lines)

            # Create a zip file containing all PNG images
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                for filename, file_content in png_files:
                    zip_file.writestr(filename, file_content)

            # Offer the zip file for download
            st.download_button('Download All PNGs', zip_buffer.getvalue(), file_name='all_cross_sections.zip',
                               mime='application/zip')

    except Exception as e:
        st.error(f'Error processing file: {e}')
else:
    st.warning('Please upload a CSV file')