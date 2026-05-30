function send() {
    const input = document.getElementById("input").value;
    const resultBox = document.getElementById("result");
  
    if (input.trim() === "") {
      resultBox.innerHTML = "재료를 입력해주세요.";
      return;
    }
  
    fetch("http://127.0.0.1:5000/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        ingredients: input
      })
    })
      .then(res => res.json())
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
            <p class="score">${item.score}점</p>
            <p>일치 재료: ${item.matched_ingredients.join(", ")}</p>
            <p>부족 재료: ${item.missing_ingredients.join(", ")}</p>
          `;
  
          resultBox.appendChild(card);
        });
      })
      .catch(error => {
        resultBox.innerHTML = "서버 연결에 실패했습니다.";
        console.error(error);
      });
  }