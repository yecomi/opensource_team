from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Server running"

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    return jsonify({"result": ["김치볶음밥", "계란말이"]})

app.run(debug=True)