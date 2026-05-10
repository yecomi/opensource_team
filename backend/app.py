from flask import Flask, request, jsonify

#서버 객체 형성//app 생성
app = Flask(__name__)


recipes = [
    {
        "name": "김치볶음밥",
        "ingredients": ["김치", "밥", "계란"]
    },
    {
        "name": "계란볶음밥",
        "ingredients": ["계란", "밥", "대파"]
    },
    {
        "name": "토스트",
        "ingredients": ["식빵", "계란", "버터"]
    }
]


@app.route('/')
def home():
    return "server running"



#/recommanend로 요청 받겠다.=>주소 만들기
@app.route('/recommend', methods=['POST'])
def recommend():
    
    data = request.json
    
    
    user_ingredients = data.get('ingredients')
    
    results = []
    
    for recipe in recipes:
        
        score = 0
        
        for ingredient in user_ingredients:
            if ingredient in recipe["ingredients"]:
                score += 1

        results.append({
            "name": recipe["name"],
            "score": score
        })
    
    results.sort(key=lambda x: x["score"], reverse=True)

    return jsonify(results)



@app.route('/test')
def test():
    
    user_ingredients = ["계란","밥"]
    
    results = []
    
    for recipe in recipes:

        score = 0

        for ingredient in user_ingredients:

            if ingredient in recipe["ingredients"]:
                score += 1

        results.append({
            "name": recipe["name"],
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return jsonify(results)

app.run(debug=True)