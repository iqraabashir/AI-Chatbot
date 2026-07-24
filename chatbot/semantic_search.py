

from sentence_transformers import SentenceTransformer, util
from sentence_transformers.util import cos_sim
from chatbot.knowledge_database import get_all_topics
from chatbot.knowledge_database import get_search_records



# Load AI model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    """
    Converts text into an AI embedding.
    """
    return model.encode(text)


def calculate_similarity(text1, text2):
    """
    Returns similarity score between two texts.
    """
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)

    similarity = cos_sim(embedding1, embedding2)

    return float(similarity[0][0])

def find_best_topic(user_question):
    records = get_search_records()

    best_topic = None
    highest_score = 0

    for topic_id, topic_name, field_name, field_value in records:
        searchable_text = f"{topic_name} {field_name} {field_value}"

        score = calculate_similarity(user_question, searchable_text)

        if score > highest_score:
            highest_score = score
            best_topic = (topic_id, topic_name)

    return best_topic, highest_score

# def find_related_topics(user_question, threshold=0.30):

#     from chatbot.knowledge_database import get_all_topics

#     query_embedding = model.encode(
#         user_question,
#         convert_to_tensor=True
#     )

#     topics = get_all_topics()

#     related_topics = []

#     for topic in topics:

#         topic_embedding = model.encode(
#             topic[1],
#             convert_to_tensor=True
#         )

#         score = util.cos_sim(
#             query_embedding,
#             topic_embedding
#         ).item()

#         if score >= threshold:
#             related_topics.append((topic, score))

#     related_topics.sort(
#         key=lambda x: x[1],
#         reverse=True
#     )

#     return related_topics