#pip install langchain sentence-transformers chromadb pandas scikit-learn

import pandas as pd
from langchain.docstore.document import Document

# Load clinical notes and insurance claims from CSV
clinical_df = pd.read_csv("clinical_notes.csv")
claims_df = pd.read_csv("insurance_claims.csv")

# Convert to LangChain Documents
clinical_docs = [
    Document(page_content= row["Clinical Note"], metadata={"patient_id": row["Patient ID"]})
    for _, row in clinical_df.iterrows()
]

claim_docs = [
    Document(page_content=row["Claim Description"], metadata={"claim_id": row["Claim ID"], "patient_id": row["Patient ID"]})
    for _, row in claims_df.iterrows()
]


from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Combine and persist
vector_db = Chroma.from_documents(clinical_docs + claim_docs, embedding_model, persist_directory="./healthcare_claims_db")
vector_db.persist()


from sklearn.metrics.pairwise import cosine_similarity

def match_claim_to_note(claim_text, patient_id):
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


flagged_df = flag_mismatched_claims(claims_df, threshold=0.5)
flagged_df.to_csv("flagged_claims.csv", index=False)
print(flagged_df.head())