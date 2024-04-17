from flask import Flask, request, jsonify, render_template
#from transformers import pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

app = Flask(__name__)

# Download the VADER lexicon
nltk.download('vader_lexicon')
# Download NLTK resources
#nltk.download('punkt')

# Initialize BERT-based emotion detection pipeline
#emotion_classifier = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/feedback_analysis')
def feedback_analysis():
    return render_template('feedback_analysis.html')

@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion_vader():
    # Get the text from the request
    text = request.json['text']

    # Perform sentiment analysis with VADER
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)

    # Determine the dominant emotion based on the sentiment scores
    dominant_emotion = determine_emotion(scores)

    # Return the emotion as JSON
    return jsonify({'emotion': dominant_emotion.capitalize()})

#helper for VADER code
def determine_emotion(scores):
    # Get the sentiment scores
    pos_score = scores['pos']
    neg_score = scores['neg']
    neu_score = scores['neu']

    # Determine the dominant emotion based on the scores
    if pos_score > neg_score and pos_score > neu_score:
        return 'happy'
    elif neg_score > pos_score and neg_score > neu_score:
        return 'sad'
    elif neu_score > pos_score and neu_score > neg_score:
        return 'neutral'
    else:
        return 'angry'


if __name__ == '__main__':
    app.run(debug=True)


"""
def analyze_emotion_bert():
    # Get the text from the request
    text = request.json['text']

    # Perform emotion detection with BERT-based model
    results = emotion_classifier(text)

    # Extract the dominant emotion
    dominant_emotion = results[0]['label']

    # Return the emotion as JSON
    return jsonify({'emotion': dominant_emotion.capitalize()})
"""