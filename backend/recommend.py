import csv
import ast
import re


def clean_ingredient(text):
    text = text.lower().strip()

    # 숫자 제거
    text = re.sub(r"\d+", "", text)

    # 단위 제거
    text = re.sub(
        r"\b(g|kg|ml|l|cup|cups|tbsp|tablespoon|tablespoons|tsp|teaspoon|teaspoons|ounce|ounces|oz|lb|pound|pounds)\b",
        "",
        text
    )

    text = text.replace("-", " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def load_foodcom_recipes(file_path="data/RAW_recipes.csv", limit=1000):
    recipes = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for idx, row in enumerate(reader):
            if idx >= limit:
                break

            try:
                ingredients = ast.literal_eval(row["ingredients"])
            except:
                continue

            cleaned_ingredients = [
                clean_ingredient(item)
                for item in ingredients
                if item.strip()
            ]

            recipes.append({
                "name": row["name"],
                "ingredients": cleaned_ingredients,
                "category": "Food.com"
            })

    return recipes


def parse_user_ingredients(user_input):
    ingredients = user_input.split(",")

    cleaned = []

    for ingredient in ingredients:
        item = clean_ingredient(ingredient)

        if item:
            cleaned.append(item)

    return list(set(cleaned))


def recommend_recipes(user_input, recipes):
    print("입력값:", user_input)
    print("파싱후:", parse_user_ingredients(user_input))
    
    user_ingredients = parse_user_ingredients(user_input)

    results = []

    for recipe in recipes:
        recipe_ingredients = recipe["ingredients"]

        matched = set(user_ingredients) & set(recipe_ingredients)
        missing = set(recipe_ingredients) - set(user_ingredients)

        if len(recipe_ingredients) == 0:
            continue

        score = len(matched) / len(recipe_ingredients) * 100

        if score > 0:
            results.append({
                "name": recipe["name"],
                "score": round(score, 1),
                "matched_ingredients": list(matched),
                "missing_ingredients": list(missing),
                "total_ingredients": len(recipe_ingredients)
            })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:10]


if __name__ == "__main__":
    recipes = load_foodcom_recipes()

    user_input = input("보유한 재료를 영어로 입력하세요. 예: egg, rice, onion\n입력: ")

    recommendations = recommend_recipes(user_input, recipes)

    print("\n추천 결과")

    for item in recommendations:
        print(f"{item['name']} - {item['score']}점")
        print(f"일치 재료: {item['matched_ingredients']}")
        print(f"부족 재료: {item['missing_ingredients']}")
        print()
print(clean_ingredient("egg"))
print(clean_ingredient("green onion"))
print(clean_ingredient("500g beef"))
print(clean_ingredient("2 cups rice"))