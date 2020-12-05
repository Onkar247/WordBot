import json
import requests
from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
import keys

app=Flask(__name__)

@app.route('/WordBot',methods=["POST"])

def WordBot():
    word_synonym = ""
    word_antonym = ""
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    message = resp.message()
    responded = False
    words = incoming_msg.split('-')

    if len(words) == 1  and incoming_msg == "help" :
        help_string = get_help_message()
        message.body(help_string)
        responded = True
    elif len(words) == 2:
        search_type = words[0].strip()
        input_string = words[1].strip().split()
        if len(input_string) == 1:
            response = get_dictionary_response(input_string[0])
            if search_type == "meaning":
                message.body(response["meaning"])
                responded = True
            if search_type == "synonyms":
                for synonym in response["synonyms"]:
                    word_synonym += synonym + "\n"
                message.body(word_synonym)
                responded = True
            if search_type == "antonyms":
                for antonym in response["antonyms"]:
                    word_antonym += antonym + "\n"
                message.body(word_antonym)
                responded = True
            if search_type == "examples":
                message.body(response["examples"])
                responded = True
    if not responded:
        message.body('Incorrect request format. Please type *help* to see the correct format')
    return str(resp)

def get_help_message():
    help=   "Improve your vocabulary of English words using *WordBot*!\n\n"\
            "Just type the things you want to know with the word: \n"\
            "*meaning* - type the word \n"\
            "*examples* - type the word \n"\
            "*synonyms* - type the word \n"\
            "*antonyms* - type the word \n"
    return help

def get_dictionary_response(word):
    word_metadata = {}
    definition = f"Sorry, definition is not available for {word}"
    example = f"Sorry, examples are not available for {word}"
    syn = [f"Sorry, synonyms are not available for {word}"]
    ant = [f"Sorry, antonyms are not available for {word}"]

    url = f'https://dictionaryapi.com/api/v3/references/thesaurus/json/{word}?key={keys.key}'
    response = requests.get(url)
    api_response = json.loads(response.text)

    if response.status_code == 200:
        for data in api_response:
            try:
                if data["meta"]["id"] == word:
                    try:
                        if len(data["meta"]["syns"]) != 0:
                            syn = data["meta"]["syns"][0]
                        if len(data["meta"]["ants"]) != 0:
                            ant = data["meta"]["ants"][0]
                        for results in data["def"][0]["sseq"][0][0][1]["dt"]:
                            if results[0] == "text":
                                definition = results[1]
                            if results[0] == "vis":
                                example = results[1][0]["t"].replace("{it}", "*").replace("{/it}", "*")
                    except KeyError as e:
                        print(e)
            except TypeError as e:
                print(e)
            break
    word_metadata["meaning"] = definition
    word_metadata["examples"] = example
    word_metadata["antonyms"] = ant
    word_metadata["synonyms"] = syn
    return word_metadata



if __name__=="__main__":
    app.run()

