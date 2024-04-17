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

    # Perform sentiment analysis with VADER
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)

    # Determine the dominant emotion based on the sentiment scores
    dominant_emotion = determine_emotion(scores)

    # Return the emotion as JSON
    return jsonify({'emotion': dominant_emotion.capitalize()})

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
