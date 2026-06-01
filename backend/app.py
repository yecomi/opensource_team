from flask_cors import CORS
from flask import Flask, request, jsonify
from recommend import load_foodcom_recipes
from recommend import recommend_recipes
#서버 객체 형성//app 생성
app = Flask(__name__)
CORS(app)
recipes = load_foodcom_recipes()
#______________자동생성 기능______________
all_ingredients = set()
for recipe in recipes:
    for ing in recipe['ingredients']:
        if ing.strip():
            all_ingredients.add(ing.strip())
unique_ingredients_list = sorted(list(all_ingredients))
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ



@app.route('/')
def home():
    return "server running"


# --- [추가] 자동완성 API 라우트 ---
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '').lower().strip()
    
    # 입력값이 너무 짧으면 빈 배열 반환
    if len(query) < 2:
        return jsonify([])
    
    # 쿼리가 포함된 재료를 최대 10개까지 매칭
    matched = [ing for ing in unique_ingredients_list if query in ing]
    return jsonify(matched[:10])
# ---------------------------------

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
    print(results)
    return jsonify(results)

app.run(debug=True)