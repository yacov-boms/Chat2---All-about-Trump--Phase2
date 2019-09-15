# spacy - Doc.similarity after stop-words, lemmatizing
from flask import Flask, request    # Has to be the first(?)
import spacy
nlp = spacy.load('en_core_web_lg')
import re
import random

app = Flask(__name__)

# A Connection to Facebook Messenger
FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'chat2secret'# <paste your verify token here>
PAGE_ACCESS_TOKEN = 'EAAVHkmOSFkEBADWfOTeqUiCDY1V9c4PeMFBJn2AuaJzISC5FNJtWW8qBhaKjhpRVsBfunft0jlx6TYVHhrEnyUZBVFSTkWfnBvNsjGSFDttxHcgcQ7D9sndUBGLk7SyvvH9eZCHNoXE8Uql5r371HD2TZCwma3C3sZAl0zkbRgZDZD'

# Read article
f=open("C://Users/Administrator/Desktop/trump2.txt",'r',errors = 'ignore')
raw=f.read()                            # string
f.close()

# Clean text
raw = re.sub("[\[].*?[\]]", "", raw)    # Drop Citations

def clean_sent(sent):
    clean_sent = [w.lemma_ for w in sent if (w.is_stop==False and not w.is_punct)]
    return nlp(' '.join(clean_sent))

text_doc = nlp(raw)
text_clean_docs = [clean_sent(sent) for sent in text_doc.sents]

# Handle Greetings
GREETING_INPUTS = ("hello", "hi", "greetings", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "Glad to talk to you"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Main Procedure
@app.route("/webhook",methods=['GET','POST'])
def listen():
    """This is the main function flask uses to listen at the `/webhook` endpoint"""
    if request.method == 'GET':             # A Webhook Check from Facebook for developers
        if  request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return "incorrect"

    if request.method == 'POST':            # A User query
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):          # Is there any content in the message?
                user_text = x['message']['text']
                user_id = x['sender']['id']
                respond(user_id, user_text)
        return "ok"

def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))

def respond(user_id, user_text):
    user_text=user_text.lower()
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get('https://graph.facebook.com/'+user_id, user_details_params).json() 

    if(user_text=='thanks' or user_text =='thank you' ):# Thanks
        send_message(user_id, "You are welcome.. "+user_details['first_name'])
        return
    if user_text == 'bye':
        send_message(user_id, "Bye Bye"+' '+user_details['first_name'])
        return
    if(greeting(user_text)!=None):                  # Greetings
        print(user_id, greeting(user_text))
        send_message(user_id, greeting(user_text)+' '+user_details['first_name'])
        return    
    else:
        query_doc = nlp(user_text)
        query_clean_doc = clean_sent(query_doc)
        sims = [query_clean_doc.similarity(text_clean_doc) for text_clean_doc in text_clean_docs]
        print('------------------ sims: ', sims)
        idx = sims.index(max(sims))
        bot_response = list(text_doc.sents)[idx]
        send_message(user_id, str(bot_response))

import requests
def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {'message': {'text': text},
               'recipient': {'id': recipient_id},
               'notification_type': 'regular'    }
    auth =    {'access_token': PAGE_ACCESS_TOKEN}
    response = requests.post(FB_API_URL, params=auth, json=payload)
    return response.json()

if __name__ == '__main__':
    print('----------- starting main  --------------')
    app.run(debug=True)

