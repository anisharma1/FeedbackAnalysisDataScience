from flask import Flask, request, render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier
import seaborn as sns
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/feedback_analysis')
def feedback_analysis():
    return render_template('feedback_analysis.html')
# Load data from text file
def load_data(file_path):
    X = []
    y = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            text, label = line.rsplit(';', 1)
            X.append(text)
            if label == 'sadness':
                y.append(0)
            elif label == 'anger':
                y.append(1)
            elif label == 'love':
                y.append(2)
            elif label == 'surprise':
                y.append(3)
            elif label == 'fear':
                y.append(4)
            elif label == 'joy':
                y.append(5)
            else:
                raise ValueError("Invalid label: {}".format(label))
    return X, y

# Load data
data_file = r'FeedbackAnalysisDataScience\train.txt'  # Adjust the file path as needed
X_train, y_train = load_data(data_file)

# Create and train the model
model = make_pipeline(
    CountVectorizer(),
    DecisionTreeClassifier()
)
model.fit(X_train, y_train)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        # Predict sentiment for the input text
        sentiment_scores = model.predict_proba([text])[0]
        sadness, anger, love, surprise, fear, joy = sentiment_scores



        return render_template('result.html', text=text, sadness=sadness, anger=anger, love=love,
                               surprise=surprise, fear=fear, joy=joy)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port = 8008)
