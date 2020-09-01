from flask import Flask, render_template, send_file, make_response
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# Enabling CORS. It is needed if we want to access our api from the frontend
CORS(app)

from app import routes