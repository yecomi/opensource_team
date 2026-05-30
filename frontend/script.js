function send() {
    const input = document.getElementById("input").value; //사용자가 입력한 재료 값 가져옴
    const resultBox = document.getElementById("result");
  
    if (input.trim() === "") { //비어있을 시 안내 문구 출
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
  
        data.forEach(item => { //추천 결과를 하나씩 반복하며 화면에 출
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
