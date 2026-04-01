from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

nom_bot = "NJK Bot"
createur = "Konnan Julius Noah"

reponses = [
    "Hmm intéressant 🤔",
    "Je vois 👀",
    "Ok je comprends 😎",
    "Bonne question 🔥"
]

def chercher(question):
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": question,
            "format": "json",
            "no_html": 1
        }

        res = requests.get(url, params=params)
        data = res.json()

        if data.get("AbstractText"):
            return data["AbstractText"]

        if data.get("RelatedTopics"):
            return data["RelatedTopics"][0].get("Text", "")

        return None
    except:
        return None

def repondre(msg):
    m = msg.lower()

    if "salut" in m:
        return "Salut 😄"

    if "nom" in m:
        return f"Je suis {nom_bot}"

    if "createur" in m:
        return f"{createur} m'a créé 🔥"

    return None

@app.route("/")
def home():
    return """
    <h1>NJK BOT 🤖🔥</h1>
    <input id="msg" placeholder="Écris ici..." />
    <button onclick="send()">Envoyer</button>
    <p id="rep"></p>

    <script>
    async function send(){
        let msg = document.getElementById("msg").value;

        let res = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: msg})
        });

        let data = await res.json();
        document.getElementById("rep").innerText = data.reply;
    }
    </script>
    """

@app.route("/chat", methods=["POST"])
def chat():
    user = request.json.get("message", "")

    rep = repondre(user)
    if rep:
        return jsonify({"reply": rep})

    net = chercher(user)
    if net:
        return jsonify({"reply": net})

    return jsonify({"reply": random.choice(reponses)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
