
from random import randint
import flask
import json
import csv
import simplenlg as snlg
from flask_cors import CORS, cross_origin


app = flask.Flask(__name__)
app.config["DEBUG"] = True

CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'


lexicon = snlg.Lexicon.getDefaultLexicon()
nlgFactory = snlg.NLGFactory(lexicon)
realiser = snlg.Realiser(lexicon)


def produce_sentence(ActionVerb: str, Subject: str, Details: [str], Results: [str]):
  verb2 = ["utilize","use","incorporate"]
  verb3 = ["lead","contribute","result","produce"]

  # preposition list is linked to verb3 list
  preposition = ["to","to","in","a"]

  # https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/
  selection = randint(0, len(verb2)-1)
  selection2 = randint(0, len(verb3)-1)
  clause1 = nlgFactory.createClause("", ActionVerb)
  clause1.setObject(nlgFactory.createNounPhrase("a", Subject))
  clause1.setFeature(snlg.Feature.TENSE, snlg.Tense.PAST)

#   clause1.setFeature(snlg.Feature.COMPLEMENTISER, "utilize")

  details_noun_phrases = [nlgFactory.createNounPhrase(detail) for detail in Details]
  list_of_details = nlgFactory.createCoordinatedPhrase()
  
  for noun_phrase in details_noun_phrases:
    list_of_details.addCoordinate(noun_phrase)

  clause2 = nlgFactory.createClause(verb=verb2[selection], directObject=list_of_details)

  clause2.setFeature(snlg.Feature.PROGRESSIVE, True)
  clause2.features["verb_phrase"].features["realise_auxiliary"] = False

  clause2.setFeature(snlg.Feature.TENSE, snlg.Tense.PRESENT)

  results_noun_phrases = [nlgFactory.createNounPhrase(result) for result in Results]
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

def cleanRequest(body):
  for key, value in list(body.items()):
      if value is "":
          del body[key]
      elif isinstance(value, dict):
          cleanRequest(value)
  return body


def to_csv():
  # Opening JSON file and loading the data 
  # into the variable data 
  with open('indeed_data.ldjson') as json_file: 
      # data = json.load(json_file) 
      data = [json.loads(line) for line in json_file]
    
  # employee_data = data['emp_details'] 
  employee_data = data
    
  # now we will open a file for writing 
  data_file = open('data_file.csv', 'w') 
    
  # create the csv writer object 
  csv_writer = csv.writer(data_file) 
    
  # Counter variable used for writing  
  # headers to the CSV file 
  count = 0
    
  for emp in employee_data: 
      if count == 0: 
    
          # Writing headers of CSV file 
          header = emp.keys() 
          csv_writer.writerow(header) 
          count += 1
    
      # Writing data of CSV file 
      csv_writer.writerow(emp.values()) 
    
  data_file.close() 
  