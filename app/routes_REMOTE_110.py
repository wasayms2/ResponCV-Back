from app import app
import flask
from helpers import produce_sentence


@app.route('/', methods=['GET'])
def home():
    return("<h1>Our Sentence Model vLatest<h1>"), 200
    
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/sentence', methods=['POST', "GET"])
def api_filter():
    content = flask.request.get_json(force=True)
    print(content)
    sentence = produce_sentence(content['ActionVerb'], content["Subject"], content["Details"], content["Results"])
    print(sentence)
    result = {"output":sentence}
    return flask.jsonify(result), 200
