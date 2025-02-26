import streamlit as st 
import pandas as pd
import os 
from io import BytesIO

# Set up our App
st.set_page_config(page_title="Smart Data Transformer", layout='wide')
st.title("🚀 Smart Data Transformer")
st.write("Easily convert and clean your CSV and Excel files with smart automation and visualization!")

uploaded_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type : {file_ext}")
            continue  

        # Display info about the file using an expander for a cleaner UI
        with st.expander(f"📜 File Details: {file.name}"):
            st.write(f"**File Name:** {file.name}")
            st.write(f"**File Size:** {file.size/1024:.2f} KB")

        # Show 5 rows of our dataframe
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠 Data Cleaning")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🗑 Remove Duplicates ({file.name})"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"📌 Fill Missing Values ({file.name})"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")

        # Choose Specific Columns to Keep or Convert
        st.subheader("📊 Column Selection")
        columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]  

        # Create Some Visualizations
        st.subheader("📈 Data Visualization")  
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Convert the File -> CSV to Excel
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)  

            # Download Button
            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All files processed successfully!")
