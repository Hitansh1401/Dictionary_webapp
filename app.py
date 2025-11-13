from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    word_data = None
    error_message = None

    if request.method == 'POST':
        word = request.form['word']
        api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()

            if isinstance(data, list) and data:

                first_entry = data[0]

                word_data = {
                    'word': first_entry.get('word'),
                    'meanings': []
                }

                for meaning in first_entry.get('meanings', []):
                    word_data['meanings'].append({
                        'partOfSpeech': meaning.get('partOfSpeech'),
                        'definitions': [
                            {'definition': d.get('definition'), 'example': d.get('example')}
                            for d in meaning.get('definitions', [])
                        ]
                    })
            else:
                error_message = "Word not found or no definitions available."

        except requests.exceptions.RequestException as e:
            error_message = f"Error connecting to the dictionary API: {e}"
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"

    return render_template('index.html', word_data=word_data, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)