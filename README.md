# Course Recommendation System

## Overview

This project implements a course recommendation system that suggests relevant courses to users based on their age, career, and budget. The recommendation system utilizes FastText for Natural Language Processing (NLP), along with other libraries such as NumPy, Pandas, NLTK, and Scikit-Learn for processing course descriptions and generating personalized recommendations.

## Table of Contents

- [Data Preparation](#data-preparation)
- [Feature Extraction](#feature-extraction)
- [User Input Processing](#user-input-processing)
- [Feature Engineering for User Input](#feature-engineering-for-user-input)
- [Model Building](#model-building)
- [Recommendation Generation](#recommendation-generation)
- [Usage](#usage)



## Data Preparation

1. **Speech-to-Text Conversion:**
   Use a Speech-to-Text tool to convert each course's video introduction into text. Consider using libraries like `speechRecognition` in Python.

2. **Video Processing:**
   Utilize `ffmpeg` or a similar tool to process the course videos and extract relevant information. This step is crucial for obtaining textual data from video content.
![speech2text.png](github%2Fspeech2text.png)
3. **Structured Format:**
   Convert the obtained data into a structured format (CSV file).

## Data Cleaning

After obtaining the video transcriptions and descriptions:

1. **Text Cleaning:**
   - Remove special characters, punctuation, and non-alphanumeric characters.
   - Convert text to lowercase.
   - Handle Unicode characters and accents using libraries like `unidecode`.
   - Remove unwanted symbols, quotes, and backslashes.

2. **Stopword Removal:**
   - Use NLTK to remove common stopwords from the text.
   - Tokenize the text into words and remove stopwords from the tokenized list.

## Feature Extraction

Utilize FastText for NLP to process course descriptions and extract relevant features. Preprocess the text using NLTK and other libraries to enhance feature extraction.

## User Input Processing

Build an input form or interface where users can input their age, career, and budget.

## Feature Engineering for User Input

Process user input using NLTK and other libraries to extract relevant features. Preprocess career information and represent it in a format that can be matched with course attributes.


## Recommendation Generation

Rank courses based on the model's output, providing the best matches for the user's age, career, and budget.


## Usage

To run the recommendation system, follow these steps:

1. Download `chromedriver.exe` and place it in the project directory.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the recommendation system using `python -m word2vec.py`.

