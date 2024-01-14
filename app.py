from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from nltk.sentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
db = SQLAlchemy(app)

# Define the Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(10), nullable=True)
    feedback = db.Column(db.Text, nullable=True)

# Create the database tables
db.create_all()

# Set up NLTK
sid = SentimentIntensityAnalyzer()

# Function to analyze sentiment
def analyze_sentiment(text):
    score = sid.polarity_scores(text)
    return 'positive' if score['compound'] >= 0 else 'negative'

# Basic route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['review_text']
        sentiment = analyze_sentiment(text)
        review = Review(text=text, sentiment=sentiment)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('result', review_id=review.id))
    return render_template('home.html')

# Route for displaying results
@app.route('/result/<int:review_id>', methods=['GET', 'POST'])
def result(review_id):
    review = Review.query.get_or_404(review_id)
    
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        review.feedback = feedback_text
        db.session.commit()

    return render_template('result.html', review=review)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
