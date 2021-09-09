from flask import Flask, request
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from bank_faq import return_faq

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

chatbot = ChatBot('Digital Teacher',
                  storage_adapter="chatterbot.storage.SQLStorageAdapter",
                  logic_adapters=[
                      {"import_path": "chatterbot.logic.BestMatch",
                       "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
                       "maximum_similarity_threshold": 0.4,
                       "default_response": "What about it?",
                       }
                  ],
                  preprocessors=[
                      'chatterbot.preprocessors.clean_whitespace',
                      'chatterbot.preprocessors.unescape_html',
                      'chatterbot.preprocessors.convert_to_ascii']
                  )

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
dialogs = return_faq()

list_trainer = ListTrainer(chatbot)
list_trainer.train(dialogs)


@app.route('/get_response', methods=["POST"])
def is_running():
    responses = chatbot.get_response(str(request.form['question']))
    return str(responses), 200


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=3001, threaded=True)
