from flask import Flask, jsonify, request
from flasgger import Swagger
import random

app = Flask(__name__)
swagger = Swagger(app)

# Liste des blagues en mémoire
jokes = [
    {"joke": "Pourquoi un canard est toujours à l'heure ? Parce qu'il est dans l'étang."},
    {"joke": "Quel est le jeu de cartes préféré des canards ? La coin-che."},
    {"joke": "Qu'est-ce qui fait Nioc nioc? Un canard qui parle en verlan."},
    {"joke": "Comment appelle-t-on un canard qui fait du DevOps ? Un DuckOps."}
]

@app.route("/joke", methods=["GET"])
def get_joke():
    """
    Renvoie une blague aléatoire
    ---
    responses:
      200:
        description: Une blague bien formulée
        examples:
          application/json: {"joke": "Pourquoi les canards n'ont pas d'ordinateur ?"}
    """
    return jsonify(random.choice(jokes))

@app.route("/joke", methods=["POST"])
def post_joke():
    """
    Ajoute une nouvelle blague
    ---
    parameters:
      - name: joke
        in: body
        required: true
        schema:
          type: object
          properties:
            joke:
              type: string
              example: "coin coin coin"
    responses:
      201:
        description: Blague enregistrée avec succès
      400:
        description: Erreur dans le format de la requête
    """
    data = request.get_json()
    if not data or "joke" not in data or len(data["joke"]) < 10:
        return jsonify({"error": "Le champ 'joke' est obligatoire et doit contenir au moins 10 caractères."}), 400
    jokes.append({"joke": data["joke"]})
    return jsonify({"message": "Blague ajoutée avec succès"}), 201

if __name__ == "__main__":
    app.run(debug=True)
