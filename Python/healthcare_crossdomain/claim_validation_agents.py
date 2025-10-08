#pip install langchain sentence-transformers chromadb pandas scikit-learn

import pandas as pd
from langchain.docstore.document import Document
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from sklearn.metrics.pairwise import cosine_similarity

# This tool creates the knowledge fabric for the clinical notes and build relationship with the patient demographics 
def create_knowledge_fabric(uploaded_df, collection_name):
    try:
        # Convert to LangChain Documents
        docs = [
            Document(page_content= row.to_csv(), metadata={"patient_id": row["Patient ID"]})
            for _, row in uploaded_df.iterrows()
        ]

        embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = Chroma.from_documents(documents=docs, embedding=embedding_model, collection_name=collection_name, persist_directory="./patient_db")
        vector_db.persist()
        msg = f"✅ Knowledge fabric creted for {collection_name} successfully."
       
    except Exception as e:
        msg = f" ❌ Error while creating knowledge fabric for {collection_name}: {e}"

    return msg


def seach_knowledge_fabric(query, collection_name, persist_directory):

    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(collection_name=collection_name, embedding_function=embedding_model,persist_directory=persist_directory) 
    #results = vectorstore.similarity_search(query=query,k=5)
    results = vectorstore.similarity_search_with_score(query=query,k=5)
    print("output from ChromaDB:")
    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:")
        print("Content:", doc.page_content)
        print("Metadata:", doc.metadata)

    return results
'''

#######

vectorstore = Chroma(collection_name=collection_name, embedding_function=embedding_model,persist_directory="./patient_db") 
all_data = vectorstore.get()
print("All documents in ChromaDB:")
for doc_content in all_data['documents']:
    print(doc_content)
#######


# validate claim description againt clinical notes
def match_claim_to_note(claims_df):

    for _, row in claims_df.iterrows():
        patient_id = row["Patient ID"]
        claim_id = row["Claim ID"]
        claim_text = row["Claim Description"]

    # Filter clinical notes for the same patient
    notes = [doc for doc in clinical_docs if doc.metadata["patient_id"] == patient_id]
    if not notes:
        return None, 0.0

    # Embed claim and notes
    claim_vec = embedding_model.embed_query(claim_text)
    note_vecs = embedding_model.embed_documents([note.page_content for note in notes])

    # Compute similarity
    scores = cosine_similarity([claim_vec], note_vecs)[0]
    best_score = max(scores)
    best_note = notes[scores.argmax()].page_content

    return best_note, best_score


def flag_mismatched_claims(claims_df, threshold=0.5):
    flagged = []

    for _, row in claims_df.iterrows():
        claim_text = row["Claim Description"]
        patient_id = row["Patient ID"]
        best_note, score = match_claim_to_note(claim_text, patient_id)

        #if score < threshold:
        flagged.append({
            "Claim ID": row["Claim ID"],
            "Patient ID": patient_id,
            "Claim Description": claim_text,
            "Best Matching Note": best_note,
            "Similarity Score": round(score, 2),
            "Status": "Rejected"
        })

    return pd.DataFrame(flagged)


'''



'''
flagged_df = flag_mismatched_claims(claims_df, threshold=0.5)
flagged_df.to_csv("flagged_claims.csv", index=False)
print(flagged_df.head())

            if uploaded_file_name == "patient_demography":
                patient_demography_df = uploaded_df
                log_container.write(" ✅ Successfully loaded patient demography")
                msg = cva.create_knowledge_fabric(uploaded_df, uploaded_file_name)
                log_container.write(msg)
            elif uploaded_file_name == "clinical_notes":
                clinical_notes_df = uploaded_df
                log_container.write(" ✅ Successfully loaded clinical notes")
                msg = cva.create_knowledge_fabric(uploaded_df, uploaded_file_name)
                log_container.write(msg)
            elif uploaded_file_name == "billing_data":
                billing_data_df = uploaded_df
                log_container.write(" ✅ Successfully loaded billing data")
                msg = cva.create_knowledge_fabric(uploaded_df, uploaded_file_name)
                log_container.write(msg)
            else:
                msg = f" ❌ Wrong file name : {uploaded_file_name} "


'''