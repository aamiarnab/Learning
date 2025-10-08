import streamlit as st
import pandas as pd
from time import sleep
from pypdf import PdfReader
import claim_validation_agents as cva


# Set page config
st.set_page_config(page_title="Claim Analysis", layout="wide")
msg=""
patient_demography_df = pd.DataFrame()
clinical_notes_df = pd.DataFrame()
billing_data_df = pd.DataFrame()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tabs
tab1, tab2, tab3 = st.tabs(["📁 Clinical Data", "📊 Validate Claim", "📈 Tab 3"])

with tab1:
    st.markdown("## Build a patient 360 knowledge fabric")
    col1, col2, col3 = st.columns([8, 1, 8])

    with col1:
        st.markdown("### Ingest data patient data")
        uploaded_file = st.file_uploader("Choose a .csv file", type=["csv"])
        st.markdown("##### Process Log")
        log_container = st.container()
        if uploaded_file:
            uploaded_file_name = uploaded_file.name[:-4]
            print("name of file: ", uploaded_file.name[:-4])
            log_container.write("uploading file ...")
            try:
                uploaded_df = pd.read_csv(uploaded_file)
            except Exception as e:
                log_container.write(f" ❌ Error reading CSV file: {e}")
                uploaded_df = pd.DataFrame()
            log_container.write(f" ✅ Successfully loaded {uploaded_file_name}")

            if uploaded_file_name in ("patient_demography", "clinical_notes", "billing_data"):
                msg = cva.create_knowledge_fabric(uploaded_df, uploaded_file_name)
                log_container.write(msg)
            else:
                msg = f" ❌ Wrong file name : {uploaded_file_name}, file name should be either of \
                    patient_demography.csv, clinical_notes.csv, billing_data.csv "

            st.markdown("### Sample Data")
            st.dataframe(uploaded_df.head(), hide_index=True)

            #msg = cva.create_clinical_notes_kf(clinical_df)
            log_container.write(msg)

    with col3:
        st.markdown("### Chat with patient data")

        chat_container = st.container(height=400)
        with chat_container:
            for chat in st.session_state.chat_history:
                role = chat["role"]
                content = chat["content"]
                st.chat_message(role).markdown(content)

        # Chat input fixed at bottom of right column
        user_input = st.chat_input("Ask a question about your data...")

        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Simulated response
            response = cva.seach_knowledge_fabric(user_input, "patient_demography", "./patient_db")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()




with tab2:
    st.markdown("## Cross validate insurance claim document and patient details ")
    col1, col2, col3 = st.columns([8, 1, 8])

    with col1:
        st.markdown("### Upload claim documnet")
        uploaded_file = st.file_uploader("Choose a .pdf file", type=["pdf"])
        st.markdown("##### Process Log")
        log_container = st.container()
        if uploaded_file:
            uploaded_file_name = uploaded_file.name[:-4]
            print("name of file: ", uploaded_file.name[:-4])
            try:
                claim_pdf = PdfReader(uploaded_file)
                claim_doc = ""
                for page_num in range(len(claim_pdf.pages)):
                    page = claim_pdf.pages[page_num]
                    claim_doc += page.extract_text()

            except Exception as e:
                log_container.write(f" ❌ Error reading pdf file: {e}")

            log_container.write(f" ✅ Successfully loaded {uploaded_file_name}")
            print(claim_doc)
            print(type(claim_doc))

            response = cva.seach_knowledge_fabric(claim_doc, "patient_demography", "./patient_db")
            #print(response)


with tab3:
    st.header("Tab 3 Content")
    st.write("This tab is reserved for future functionality.")