from flask import Flask, request, jsonify
from flask_cors import CORS  
import spacy

app = Flask(__name__)
CORS(app) 

nlp = spacy.load("en_core_web_sm")

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json()
    intent = req["queryResult"]["intent"]["displayName"]
    query = req["queryResult"]["queryText"]

    if intent == "Order Status":
        response_text = "Your order is being processed. You'll receive updates shortly."
    elif intent == "Product Info":
        response_text = "Our product is top quality and available in various colors."
    elif intent == "Refund":
        response_text = "Would you like more info about getting a refund, we can also offer you credit"
    elif intent == "Bye":
        response_text = "Thank you, feel free to chat some more"
    elif intent == "Price":
        response_text = "Price depends on size of product selected"
    else:
        doc = nlp(query)
        response_text = f"I'm not sure about that. Can you provide more details? I detected these keywords: {[token.text for token in doc if token.is_alpha]}"

    return jsonify({
        "fulfillmentText": response_text
    })

if __name__ == "__main__":
    app.run(port=5000)
