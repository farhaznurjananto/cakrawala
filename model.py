import re
import os
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from sklearn.feature_extraction.text import TfidfVectorizer

def predict(inputData):
    def load_data(folder_path):
        texts = []
        labels = []
        for label in ['human-written', 'ai-generated']:
            path = os.path.join(folder_path, label)
            for filename in os.listdir(path):
                with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:
                    texts.append(file.read())
                    labels.append(1 if label == 'ai-generated' else 0)
        return texts, labels

    data, labels = load_data('dataset_cakrawala')

    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000)
    tokenizer.fit_on_texts(data)
    sequences = tokenizer.texts_to_sequences(data)

    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_df=0.7)
    X = tfidf.fit_transform(data).toarray()

    user_input = inputData

    user_input_features = tfidf.transform([user_input]).toarray()

    loaded_model = load_model('training_model_terbaik.h5')

    prediction = loaded_model.predict(user_input_features)
    ai_generated_percentage = prediction[0][0] * 100
    human_written_percentage = (1 - prediction[0][0]) * 100

    threshold = 0.5
    if prediction > threshold:
        input_type = "AI-generated"
    else:
        input_type = "Human-written"

    sentences = re.split(r'(?<=[.!?]) +', user_input)
    ai_generated_sentences = []

    for sentence in sentences:
        sentence_features = tfidf.transform([sentence]).toarray()
        sentence_prediction = loaded_model.predict(sentence_features)
        if sentence_prediction > threshold:
            ai_generated_sentences.append(sentence)

    if ai_generated_sentences:
        print("Kalimat yang terindikasi buatan AI:")
        for sentence in ai_generated_sentences:
            print(f"- {sentence}")

    dataReturn = {'result': input_type, 'ai_precentage': ai_generated_percentage, 'human_precentage': human_written_percentage, 'list_ai_sentences': ai_generated_sentences}
    return dataReturn

