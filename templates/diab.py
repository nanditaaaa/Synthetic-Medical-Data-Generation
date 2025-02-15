# -*- coding: utf-8 -*-
"""Untitled10.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11YBvDhi0OLxcccOkwriaSFSJ7tL3JAC3
"""

# Step 1: Data Preprocessing
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load the dataset
data = pd.read_csv("Diabetes.csv")
data.head()

# Check for missing values
print(data.isnull().sum())

# Handle missing values (assuming forward fill for simplicity)
data.fillna(method='ffill', inplace=True)

# Drop any remaining NaN values if present
data.dropna(inplace=True)

# Separate the target variable
y = data['Diabetes_012']

# Create a copy of the data without the target variable
X = data.drop(columns=['Diabetes_012'])

# Select the first 10,000 data points
X_subset = X[:1000]
y_subset = y[:1000]

# Combine X_subset and y_subset to form the revised dataset
orginal_data = pd.concat([X_subset, y_subset], axis=1)

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_subset, y_subset, test_size=0.2, random_state=42)

# Function for text preprocessing
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # Join tokens back into a string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

# Iterate over columns and apply preprocessing
for col in X.columns:
    if X[col].dtype == 'object':  # Check if column is of type object (text)
        X[col] = X[col].apply(preprocess_text)

# Encode categorical variables
X = pd.get_dummies(X)

# Scale numerical features
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
numerical_columns = X.select_dtypes(include=['float64', 'int64']).columns
X[numerical_columns] = scaler.fit_transform(X[numerical_columns])

"""# **Exploratory Data Analysis (EDA)**"""

# Step 2: Exploratory Data Analysis (EDA)
print(X.describe())

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input, Reshape, Flatten, Dot, Add
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

# Define the dimensions of the input noise vector
latent_dim = 100

# Define the attention layer
def attention_layer(x):
  # Attention mechanism with a single attention head
  attention_weights = Dense(128, activation='softmax')(x)  # Change the shape to match x
  attention_weights = Reshape((x.shape[-1],))(attention_weights)  # Reshape to match x shape
  context_vector = Dot(axes=1)([attention_weights, x])
  output = Add()([x, context_vector])  # Add weighted features to original input
  return output

# Define the generator model with attention
def build_generator(latent_dim):
  input_noise = Input(shape=(latent_dim,))
  x = Dense(128, activation='relu')(input_noise)
  x = attention_layer(x)  # Apply attention layer
  x = Dense(256, activation='relu')(x)
  x = Dense(512, activation='relu')(x)
  output = Dense(data.shape[1], activation='sigmoid')(x)  # Output layer matches data dimension
  generator = Model(inputs=input_noise, outputs=output)
  return generator

# Define the discriminator model
def build_discriminator(input_shape):
    input_data = Input(shape=input_shape)
    x = Dense(512, activation='relu')(input_data)
    x = Dense(256, activation='relu')(x)
    x = Dense(128, activation='relu')(x)
    output = Dense(1, activation='sigmoid')(x)
    discriminator = Model(inputs=input_data, outputs=output)
    discriminator.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0002, beta_1=0.5), metrics=['accuracy'])
    return discriminator

# Compile the discriminator
discriminator = build_discriminator(input_shape=(data.shape[1],))
discriminator.trainable = False

# Build the GAN model
generator = build_generator(latent_dim)
gan_input = Input(shape=(latent_dim,))
synthetic_data = generator(gan_input)
gan_output = discriminator(synthetic_data)
gan = Model(gan_input, gan_output)
gan.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0002, beta_1=0.5))

# Training the GAN
def train_gan(data, generator, discriminator, gan, latent_dim, epochs=500, batch_size=128):
    for epoch in range(epochs):
        # Sample random noise for generator input
        noise = np.random.normal(0, 1, (batch_size, latent_dim))

        # Generate synthetic data
        generated_data = generator.predict(noise)

        # Select a random batch of real data
        idx = np.random.randint(0, data.shape[0], batch_size)
        real_data = data[idx]

        # Train the discriminator
        d_loss_real = discriminator.train_on_batch(real_data, np.ones((batch_size, 1)))
        d_loss_fake = discriminator.train_on_batch(generated_data, np.zeros((batch_size, 1)))
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        # Train the generator (via the GAN model)
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        valid_labels = np.ones((batch_size, 1))
        g_loss = gan.train_on_batch(noise, valid_labels)

        # Print progress
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Discriminator Loss: {d_loss[0]}, Generator Loss: {g_loss}")

# Train the GAN
train_gan(data.values.astype('float32'), generator, discriminator, gan, latent_dim)

# Generate synthetic data using the trained generator model
import random
from sklearn.model_selection import train_test_split

# Define the number of synthetic samples to generate
num_synthetic_samples = len(data)  # Generate as many synthetic samples as the original data

# Generate random noise for the generator input
noise = np.random.normal(0, 1, (num_synthetic_samples, latent_dim))

# Generate synthetic data
synthetic_data = generator.predict(noise)

# Convert synthetic_data to DataFrame
synthetic_df = pd.DataFrame(synthetic_data)

# Now, synthetic_df contains the generated synthetic data
print(synthetic_df.head())

# Separate the target variable
y = synthetic_data[:, 0]

# Create a copy of the data without the target variable
X = synthetic_data[:, 1:]

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_subset, y_subset, test_size=0.2, random_state=42)

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_reg = LogisticRegression(max_iter=1000)
log_reg.fit(X_train_scaled, y_train)

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import numpy as np
import pickle

# Assuming log_reg is your trained logistic regression model
# and it has been loaded from a pickle file or defined elsewhere in your code

# Your input data
input_data = [int(x) for x in "1 1 45 0 0 0 1 0 1 1 5".split(' ')]

# Reshape the input data to be a 2D array with one row (since it's a single sample)
input_array = np.array(input_data).reshape(1, -1)

# Make the prediction
predictions = log_reg.predict_proba(input_array)

# Extract the probability of the second class
second_class_probability = predictions[0][1]

# Print the probability of the second class
print(second_class_probability)

import pickle

pickle.dump(log_reg,open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))