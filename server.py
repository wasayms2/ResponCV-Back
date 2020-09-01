# This is the old server file.
# It is not being used but the code needs to be ported over



# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:02:45 2020

@author: Adam Salyers
"""
from random import randint
import flask
import simplenlg as snlg
from flask_cors import CORS, cross_origin
import pandas as pd


app = flask.Flask(__name__)
app.config["DEBUG"] = True

CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'


lexicon = snlg.Lexicon.getDefaultLexicon()
nlgFactory = snlg.NLGFactory(lexicon)
realiser = snlg.Realiser(lexicon)

to_csv()


'''
Betsy - updated
'''
# edit on Shahmeer's code

def produce_sentence(action_verb: str, subject: str, details: list, results: list):
  verb2 = ["utilize","use","incorporate"]
  verb3 = ["lead","contribute","result","produce"]

  # preposition list is linked to verb3 list
  preposition = ["to","to","in","a"]

  # https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/
  selection = randint(0, len(verb2)-1)
  selection2 = randint(0, len(verb3)-1)
  clause1 = nlgFactory.createClause("", action_verb)
  clause1.setObject(nlgFactory.createNounPhrase("a", subject))
  clause1.setFeature(snlg.Feature.TENSE, snlg.Tense.PAST)

#   clause1.setFeature(snlg.Feature.COMPLEMENTISER, "utilize")

  details_noun_phrases = [nlgFactory.createNounPhrase(detail) for detail in details]
  list_of_details = nlgFactory.createCoordinatedPhrase()
  
  for noun_phrase in details_noun_phrases:
    list_of_details.addCoordinate(noun_phrase)

  clause2 = nlgFactory.createClause(verb=verb2[selection], directObject=list_of_details)

  clause2.setFeature(snlg.Feature.PROGRESSIVE, True)
  clause2.features["verb_phrase"].features["realise_auxiliary"] = False

  clause2.setFeature(snlg.Feature.TENSE, snlg.Tense.PRESENT)

  results_noun_phrases = [nlgFactory.createNounPhrase(result) for result in results]
  list_of_results = nlgFactory.createCoordinatedPhrase()
  
  for noun_phrase in results_noun_phrases:
    list_of_results.addCoordinate(noun_phrase)

  clause3 = nlgFactory.createClause(verb=verb3[selection2], directObject=list_of_results)

  # removed 'to'
  clause3.setIndirectObject(preposition[selection2])
  clause3.setFeature(snlg.Feature.PROGRESSIVE, True)
  clause3.features["verb_phrase"].features["realise_auxiliary"] = False
  clause3.setFeature(snlg.Feature.TENSE, snlg.Tense.PRESENT)

  sentence = nlgFactory.createCoordinatedPhrase()
  sentence.setFeature(snlg.Feature.CONJUNCTION, "")
  sentence.addCoordinate(clause1)
  sentence.addCoordinate(clause2)
  sentence.addCoordinate(clause3)
  return realiser.realiseSentence(sentence)
    

@app.route('/', methods=['GET'])
def home():
    return("<h1>Our Sentence Model vLatest<h1>"), 200
    
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/sentences', methods=['POST', "GET"])
def api_filter():
    content = flask.request.get_json(force=True)
    print(content)
    sentence = produce_sentence(content['action_verb'], content["subject"], content["details"], content["results"])
    print(sentence)
    result = {"output":sentence}
    return flask.jsonify(result), 200

app.run(port=5000, host="0.0.0.0")
