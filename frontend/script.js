let ingredients = [];
function send() {
    const input = ingredients.join(",");
    const resultBox = document.getElementById("result");

    if (ingredients.length === 0) {
      resultBox.innerHTML = "재료를 입력해주세요.";
      return;
    }
    fetch("http://127.0.0.1:5000/recommend", { //Flask 백엔드 서버의 /recommend API로 요청 보냄
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ //입력한 재료를 JSON형식으로 서버에 전달
        ingredients: input
      })
    })
      .then(res => res.json()) //서버 응답을 JSON형태로 변환
      .then(data => {
        resultBox.innerHTML = "";
  
        if (!data || data.length === 0) {
          resultBox.innerHTML = "추천 가능한 요리가 없습니다.";
          return;
        }
  
          data.forEach(item => {

            const card = document.createElement("div");

            card.className = "recipe-card";

            card.innerHTML = `
              <h3>${item.name}</h3>

              <p class="score">
                일치도 : ${item.score}%
              </p>

              <p>
                일치 재료 :
                ${item.matched_ingredients.join(", ")}
              </p>

              <p>
                부족 재료 :
                ${item.missing_ingredients.join(", ")}
              </p>

              <details>

                <summary>
                  레시피 보기
                </summary>


                <h4>재료</h4>

                <ul>
                  ${item.ingredients.map(
                    ingredient =>
                    `<li>${ingredient}</li>`
                  ).join("")}
                </ul>

                <h4>조리순서</h4>

                <ol>
                  ${item.steps.map(
                    step =>
                    `<li>${step}</li>`
                  ).join("")}
                </ol>

              </details>
            `;

            resultBox.appendChild(card);

          });
      })
      .catch(error => {
        resultBox.innerHTML = "서버 연결에 실패했습니다.";
        console.error(error);
      });
  }
  function addIngredient() {

    const input =
        document.getElementById("ingredientInput");

    const value =
        input.value.trim();

    if(value === "")
        return;

    ingredients.push(value);

    renderIngredients();

    input.value = "";
}


function renderIngredients() {

    const list =
        document.getElementById("ingredientList");

    list.innerHTML = "";

    ingredients.forEach((item,index)=>{

        const tag =
            document.createElement("span");

        tag.className =
            "ingredient-tag";

        tag.innerHTML =
            `${item}
             <button onclick="removeIngredient(${index})">
             ×
             </button>`;

        list.appendChild(tag);
    });
}


function removeIngredient(index){

    ingredients.splice(index,1);

    renderIngredients();
}
async function handleAutocomplete(query) {

    const list =
        document.getElementById("autocompleteList");

    if(query.length < 2){

        list.innerHTML = "";
        return;
    }

    try{

        const response =
            await fetch(
                `http://127.0.0.1:5000/autocomplete?q=${query}`
            );

        const data =
            await response.json();

        list.innerHTML = "";

        data.forEach(item=>{

            const div =
                document.createElement("div");

            div.className =
                "suggestion-item";

            div.innerText =
                item;

            div.onclick = ()=>{

                document.getElementById(
                    "ingredientInput"
                ).value = item;

                list.innerHTML = "";
            };

            list.appendChild(div);
        });

    }
    catch(error){

        console.error(error);
    }
}
