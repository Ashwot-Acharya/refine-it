from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('roberta-base')


def analyze_sentence(text1, text2 , text3 ):

    texts = [text1 , text2 , text3]
    embeddings = model.encode(texts, convert_to_tensor=True)

    # Compute similarity scores
    similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)
    print("Similarity Matrix:")
    print(similarity_matrix)
        