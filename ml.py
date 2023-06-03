import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import DPRContextEncoder

def get_similar_text_andDoctor_list():

    encoder = SentenceTransformer("pritamdeka/S-PubMedBert-MS-MARCO")

    df = pd.read_csv('updated_output.csv')

    df['Speciality'] = df['Speciality'].apply(lambda x: x.split(', '))
    merged_list = list(set([item for sublist in df['Speciality'] for item in sublist]))
    text = merged_list
    vectors = encoder.encode(text)

    vector_dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(vector_dimension)
    faiss.normalize_L2(vectors)
    index.add(vectors)

    query_text = "Acute Conjunctivitis"

    # Encode the query text
    query_vector = encoder.encode([query_text])

    # Search for similar text
    k = 5  # Number of nearest neighbors to retrieve
    distance, indices = index.search(query_vector, k=10)
    print(distance)
    # Retrieve the similar text based on the indices
    similar_text = [merged_list[i] for i in indices[0]]

    very_similar = similar_text[0:5]
    less_similar = similar_text[6:10]

    final_df = pd.DataFrame(columns=['Doctor', 'url', 'Speciality', 'Address', 'Distance(miles)', 'Timings', 'Insurance'])

    for i in similar_text:
        temp_df = df[df['Speciality'].apply(lambda x: i in x)]
        final_df = pd.concat([final_df, temp_df], ignore_index=True)

    final_df = final_df.drop_duplicates(subset=['Doctor'])
    print(similar_text)
    print(final_df)
    return similar_text, final_df