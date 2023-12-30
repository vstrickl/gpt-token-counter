import spacy
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

def find_answer(processed_text, question):
    doc = nlp(processed_text)
    question_doc = nlp(question)
    # Example logic: find the sentence in the document that is most similar to the question
    most_similar_sentence = None
    highest_similarity = 0
    for sentence in doc.sents:
        similarity = sentence.similarity(question_doc)
        if similarity > highest_similarity:
            highest_similarity = similarity
            most_similar_sentence = sentence.text
    return most_similar_sentence if most_similar_sentence else "No relevant information found."