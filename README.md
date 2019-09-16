# Chat2 - Phase 2
All about Trump - A light Chatbot with agile approach
This chatbot is for human language messaging  interacion. 
It provides factual answers for various users queries about President Donald Trump.
The heart of the chatbot is a Python program with spacy package residing (currently) on a local computer.
It is also comprised of:
•	Flask - A python local web server which listens to messages from Facebook Messenger. 
•	Requests - A python package for sending messages back to users.
•	Ngrok- A safe https connection from the local web server to Facekook Messenger.
•	It uses Facekook Messenger connectivity, which has over 1 billion users.

Chatbot Funcionality:
At startup:
•	loads model en_core_web_lg 
•	Establishes connection with Messenger
•	Reads a text file
•	applies NLP function to create a semantic doc object
•	Does cleaning and lemmatazaion

In response to a users query:
•	Possible basic rule based greetings
•	Creates a semantic query object
•	Checks cosine similarity between the query and each of the file's sentences 
Based on the English large model semantics.
•	Picks the best similar sentence and sends it to the user.

Results:
Significant improvement over phase1 by tracking semantic similarities.


