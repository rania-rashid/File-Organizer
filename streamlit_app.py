import streamlit as st
from file_organizer_automation import organize_files
from pathlib import Path

st.title("File Organizer")

folder_input = st.text_input("Folder to organize", value=str(Path.home() / "Downloads"))
dry_run = st.checkbox("Dry run (preview only, don't move anything)")

if st.button("Run"):
    results = organize_files(Path(folder_input), dry_run=dry_run)
    st.write(f"Processed {len(results)} files")
    st.dataframe(results)