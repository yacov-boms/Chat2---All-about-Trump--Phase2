# Chat2 - Phase 2  
All about Trump - A light Chatbot with agile approach  
This chatbot is for human language messaging  interaction.   
It provides factual answers for various users queries about President Donald Trump.  
The heart of the chatbot is a **Python program with spacy package** residing (currently) on a local computer.  
It is also comprised of:  
*	_Flask_ - A python local web server which listens to messages from Facebook Messenger. 
*	_Requests_ - A python package for sending messages back to users.
*	_Ngrok_ - A safe https connection from the local web server to Facebook Messenger.
*	It uses _Facebook Messenger_ connectivity, which has over 1 billion users.

## Chatbot Functionality:  
**At startup:**  
*	**loads model en_core_web_lg** 
*	Establishes connection with Messenger
* Reads a text file
*	applies NLP function to create a semantic doc object
*	Does cleaning and lemmatazaion

**In response to a users query:**  
*	Possible basic rule based greetings
*	Creates a semantic query object
*	**Checks cosine similarity** between the query and each of the file's sentences  
  based on the **English large model semantics.**
*	Picks the best similar sentence and sends it to the user

**Results:**  
**Significant improvement over phase1 by tracking semantic similarities.**  



