from flask import Flask, request, jsonify, render_template
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

app = Flask(__name__)

# Download the VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/feedback_analysis')
def feedback_analysis():
    return render_template('feedback_analysis.html')


@app.route('/analyze_emotion', methods=['POST'])
def analyze_emotion():
    # Get the text from the request
    text = request.json['text']
    
    # Perform sentiment analysis
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    dominant_emotion = max(scores, key=scores.get)
    
    # Return the emotion as JSON
    return jsonify({'emotion': dominant_emotion.capitalize()})

if __name__ == '__main__':
    app.run(debug=True)
