from flask_cors import CORS
from flask import Flask, request, jsonify
from recommend import load_foodcom_recipes
from recommend import recommend_recipes
#서버 객체 형성//app 생성
app = Flask(__name__)
CORS(app)
recipes = load_foodcom_recipes()




@app.route('/')
def home():
    return "server running"




#/recommanend로 요청 받겠다.=>주소 만들기
@app.route('/recommend', methods=['POST'])
def recommend():

    data = request.json

    user_input = data.get('ingredients')

    print(user_input)
    print(type(user_input))
    
    results = recommend_recipes(user_input, recipes)

    return jsonify(results)



@app.route('/test')
def test():

    results = recommend_recipes(
        "egg,rice,onion",
        recipes
    )

    return jsonify(results)

app.run(debug=True)