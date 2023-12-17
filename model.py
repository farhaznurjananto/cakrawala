import re
import os
# import tensorflowjs as tfjs
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D  # Update TensorFlow imports
from sklearn.feature_extraction.text import TfidfVectorizer

def predict(inputData):
    # 1. Load Data from txt files
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

    # 2. Tokenize text data
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=10000)  # Adjust num_words as needed
    tokenizer.fit_on_texts(data)
    sequences = tokenizer.texts_to_sequences(data)

    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_df=0.7)
    X = tfidf.fit_transform(data).toarray()  # Convert to numpy array
    # X = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=100)  # Adjust maxlen as needed

    # # Convert labels to numpy array
    # y = np.array(labels)

    # # 3. Train-test split
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # # 4. Define and compile the Keras model
    # model = Sequential([
    #     Embedding(input_dim=10000, output_dim=64, input_length=100),
    #     GlobalAveragePooling1D(),
    #     Dense(1, activation='sigmoid')
    # ])
    # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # # Training with early stopping if accuracy does not improve for 3 epochs
    # early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=100, mode='max', verbose=1)

    # # 5. Train the model
    # history = model.fit(X_train, y_train, epochs=10000, batch_size=32, validation_data=(X_test, y_test), callbacks=[early_stopping])

    # # Define the file names
    # h5_file = 'best_trained_model.h5'
    # tfjs_dir = 'tfjs_model'

    # # Check if the HDF5 and TensorFlow.js file already exists
    # if (not os.path.exists(h5_file)) and (not os.path.exists(tfjs_dir)):
    #     # 6. Save the Keras model in HDF5 format (.h5)
    #     model.save('best_trained_model.h5')

    #     # 7. Convert the Keras model to TensorFlow.js format
    #     tfjs.converters.save_keras_model(model, 'tfjs_model')

    # Script 1: (Your existing code remains unchanged)

    # Script 2 (Revised):


    # Assuming you have a tfidf object defined for text transformation

    # Input user text for prediction
    user_input = inputData

    # Preprocess the user input similar to the training data
    # user_input_features = tokenizer.texts_to_sequences([user_input])
    # user_input_features = tf.keras.preprocessing.sequence.pad_sequences(user_input_features, maxlen=100)

    user_input_features = tfidf.transform([user_input]).toarray() # Load the trained model for prediction

    # Load the trained model for prediction
    loaded_model = load_model('training_model_terbaik.h5')

    # Predict whether the input is AI-generated or human-written
    prediction = loaded_model.predict(user_input_features)
    ai_generated_percentage = prediction[0][0] * 100
    human_written_percentage = (1 - prediction[0][0]) * 100

    # present
    # ai_generated_percentage = float(ai_generated_percentage)
    # human_written_percentage = float(human_written_percentage)

    # Determine if input is AI-generated or human-written based on a threshold
    threshold = 0.5
    if prediction > threshold:  # Adjusted variable name to prediction
        input_type = "AI-generated"
    else:
        input_type = "Human-written"

    # Display the percentages of AI-generated and human-written text
    print(f"Persentase teks hasil AI: {ai_generated_percentage:.2f}%")
    print(f"Persentase teks buatan manusia: {human_written_percentage:.2f}%")

    # Display the conclusion based on the threshold
    print(f"Teks cenderung buatan: {input_type}")

    # Find sentences with high AI-generated probability
    sentences = re.split(r'(?<=[.!?]) +', user_input)
    ai_generated_sentences = []

    for sentence in sentences:
        # sentence_features = tokenizer.texts_to_sequences([sentence])
        sentence_features = tfidf.transform([sentence]).toarray()
        # sentence_features = tf.keras.preprocessing.sequence.pad_sequences(sentence_features, maxlen=100)
        sentence_prediction = loaded_model.predict(sentence_features)
        if sentence_prediction > threshold:  # Adjusted variable name to sentence_prediction
            ai_generated_sentences.append(sentence)

    # Display AI-generated sentences
    if ai_generated_sentences:
        print("Kalimat yang terindikasi buatan AI:")
        for sentence in ai_generated_sentences:
            print(f"- {sentence}")

    dataReturn = {'result': input_type, 'ai_precentage': ai_generated_percentage, 'human_precentage': human_written_percentage, 'list_ai_sentences': ai_generated_sentences}
    return dataReturn

