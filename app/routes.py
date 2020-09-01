from app import app
import flask, PyPDF2
# from io import StringIO
from reportlab.pdfgen import canvas
from helpers import produce_sentence, cleanRequest, to_csv
from flask import make_response
from io import BytesIO

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


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

@app.route('/preview', methods = ['GET'])
def process_request():
    output = StringIO

    p = canvas.Canvas(output)
    p.drawString(100, 100, 'Hello')
    p.showPage()
    p.save()
        
    pdf_out = output.getvalue()
    output.close()

    response = make_response(pdf_out)
    response.headers['Content-Disposition'] = "attachment; filename='temp.pdf"
    response.mimetype = 'application/pdf'
    return response 
