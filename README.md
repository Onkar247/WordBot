# WordBot
A WhatsApp Chatbot to improve English vocabulary

# Steps to follow

* Clone this project
* Create a Twilio Account to get access to the Twilio API through which you can integrate this chatbot with WhatsApp
* Install 'ngrok' to connect the flask application running on your local server to the public URL that Twilio can connect to 
* Connect your smartphone with an active WhatsApp number to the Twilio WhatsApp Sandbox
* Create an account on Merriam-Webster Developer Center to get the API Key for Merriam-Webster Thesaurus API
* Add this API Key to API request in app.py file and save changes
* Run this project 
* On second terminal, go folder where ngrok is installed and start ngrok at the same port on which app.py is listening
* Go back to the Twilio Console, click on Programmable SMS > WhatsApp > Sandbox
* Copy the https:// URL from the ngrok output and then paste it to twilio's input field
* Add the URL displayed on second terminal and set the request Method to *HTTP POST* and save changes
* Send 'help' text from your verified WhatsApp number to Chatbot 
* Now you are good to go with this Chatbot 
