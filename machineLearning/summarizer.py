from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=2000, min_length=30, length_penalty=2.0):
    
    summary = summarizer(
        text,
        max_length=max_length,
        min_length=min_length,
        length_penalty=length_penalty,
        do_sample=False
    )
    return summary[0]['summary_text']


def split_text_into_chunks(text, chunk_size=1024):
    
    sentences = text.split(". ")
    chunks = []
    current_chunk = []

    for sentence in sentences:
        if len(" ".join(current_chunk)) + len(sentence) <= chunk_size:
            current_chunk.append(sentence)
        else:
            chunks.append(". ".join(current_chunk))
            current_chunk = [sentence]
    
    if current_chunk:
        chunks.append(". ".join(current_chunk))
    
    return chunks



