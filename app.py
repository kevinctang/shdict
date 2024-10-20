from flask import Flask, render_template, request
import pandas as pd

# Load the dataset
df = pd.read_csv('Projects/SHDict/sh_dictionary.csv')  # Replace with your dataset path

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for word search
@app.route('/search')
def search():
    query = request.args.get('word')
    if query:
        # Filter words that contain the search query in the 'word' column
        result_word = df[df['word'].str.contains(query, case=False, na=False)]

        # Filter words that contain the search query in the 'definition' column
        result_definition = df[df['definition'].str.contains(query, case=False, na=False)]

        # Exclude entries that already appear in result_word to avoid duplication
        more_results = result_definition[~result_definition['word'].isin(result_word['word'])]

        return render_template(
            'results.html', 
            word=query, 
            results=result_word.to_dict('records'),
            more_results=more_results.to_dict('records')  # Pass secondary results separately
        )
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
