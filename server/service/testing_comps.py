from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def is_question_similar(new_question, question_list, threshold=0.7):
    model = SentenceTransformer('multi-qa-MiniLM-L6-dot-v1')

    # Get embeddings for the new question and the existing questions
    new_question_embedding = model.encode(new_question)
    question_list_embeddings = model.encode(question_list)

    # Calculate cosine similarity between the new question and each question in the list
    similarities = cosine_similarity([new_question_embedding], question_list_embeddings)

    # Check if any similarity is above the threshold
    for similarity_value in similarities[0]:
        if similarity_value > threshold:
            return True
    return False

def check_string_in_list(lst, s):
    for item in lst:
        if item in s:
            return True
    return False

# Example usage
if __name__ == "__main__":
    # Test is_question_similar
    new_question = "Rosie can you please lift your your arms for me?"
    question_list = [
        "Rosie, raise your arms",
        "Rosie, elevate your arms",
        "Rosie, lift up your arms",
        "Rosie, hoist your arms",
        "Rosie, pick up your arms",
        "Rosie, put your arms up",
        "Rosie, straighten your arms",
        "Rosie, reach for the sky",
        "Rosie, stretch your arms",
        "Rosie, extend your arms",
    ]
    similar = is_question_similar(new_question, question_list)
    print(f"is_question_similar: {similar}")  # Expected output: False (no question is similar enough)

    # Test check_string_in_list
    lst = ["apple", "banana", "orange"]
    s = "I like bananas"
    contains = check_string_in_list(lst, s)
    print(f"check_string_in_list: {contains}")  # Expected output: True (the string "banana" is a substring of "I like bananas")
