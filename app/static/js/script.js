const modal = document.querySelector('#modal');
const btn = document.querySelector('#openModal');
const close1 = document.querySelector('#close1');
const close2 = document.querySelector('#close2');
const close3 = document.querySelector('#close3');
const getStart = document.querySelector('#btnGetStart');
const modalMain = document.querySelector('#modalMain');
const question = document.querySelector('#mainQuestion');
const modalQuestion = document.querySelector('#modalQuestion');
const resultsBox = document.querySelector('.result-box');
const chatBoxBC = document.querySelector('.chatInputBc');
const sentBtn = document.querySelector('#btnChat');
const chatInput = document.querySelector('.chatInput textarea');
const chatBox = document.querySelector('.chatBox');
const textarea = document.querySelector('#textarea');
const voiceBtn = document.querySelector('#VoiceChat');




var record = true;


// ChatBox
async function GenerateResponseToMessage(b) {
  let response = await eel.getUserMessage(b)();
  return response
}



// Возможный запрос сверху инпута. Изменить
async function ForResultBox(text){
    const results_for_box = await eel.results_box(text)();
    if (!results_for_box){
    resultsBox.style.height = "0";
    chatBoxBC.style.borderTopRightRadius = "0";
    chatBoxBC.style.borderTopLeftRadius = "0";
    }
    else if(results_for_box.length){
        console.log(results_for_box);
        resultsBox.innerHTML = "<ul type='none'>"+ results_for_box.join('') +"</ul>";
        if (resultsBox.style.height === "0px") {
        chatBoxBC.style.borderTopRightRadius = `${20}px`;
        chatBoxBC.style.borderTopLeftRadius = `${20}px`;
        resultsBox.style.height = `${ resultsBox.scrollHeight }px`;
        console.log(resultsBox.scrollHeight);
    }
    }
}
// выбрать возможный ответ
function selectInput(new_value){
      textarea.value = new_value[0].replace(/_/g, " ");
      sentBtn.click();
}



textarea.addEventListener('input', function(){
       if (textarea.value.trim().length > 0) {
            sentBtn.style.display = 'block';
            VoiceChat.style.display = 'none';
            ForResultBox(textarea.value);
       }
       else{
            sentBtn.style.display = 'none';
            VoiceChat.style.display = 'block';
            }
});


let userMessage;

const createChatLi = (message, className) => {
  const chatLi = document.createElement('li');
  chatLi.classList.add('chat', className);
  let chatContent = className === 'chatOutgoing' ? `<p>${message}</p>` : `<p>${message}</p>`;

  chatLi.innerHTML = chatContent;
  return chatLi;
};


// Отправить
async function ResponseToMessage()  {
        record = false;
        resultsBox.innerHTML = '';
        timer.style.display = 'none';
        sentBtn.style.display = 'none';
        VoiceChat.style.display = 'block';
        resultsBox.style.height = "0";
        chatBoxBC.style.borderTopRightRadius = "0";
        chatBoxBC.style.borderTopLeftRadius = "0";
        userMessage = chatInput.value.trim();
        if (!userMessage) return;
        chatBox.appendChild(createChatLi(userMessage, 'chatOutgoing'));
        let message_to_response = textarea.value;
        textarea.value = '';
        console.log(`${message_to_response}`)


        // POST-запрос
        const request = new Request("http://127.0.0.1:8000/api/message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text_content: `${message_to_response}` }),
        });
        const response1 = await fetch(request);
        const data = await response1.json();
        console.log(data    );
        chatBox.appendChild(createChatLi(data['response'], 'chatIncoming'));

}

async function RecordVoice(){
  record = true;
  console.log('возня');

  const request = new Request("/api/voice/start_voice/1", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
  });

  sentBtn.style.display = 'block';
  VoiceChat.style.display = 'none';
  while (record) {
      const response = await fetch('/api/voice/recognize/');
      const data = await response.json();
      if (response.status === 200) {
          textarea.value = data.result;
      } else {
          break;
      }
      await new Promise(resolve => setTimeout(resolve, 10)); // Пауза в 1 секунду
  }
  textarea.value = ''
}






VoiceChat.onclick = function () {
timer.style.display = 'block';
textarea.style.width = '71%';
textarea.style.margin = '24px 0 24px 0';
};



document.addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    sentBtn.click();
  }
});

sentBtn.addEventListener('click', ResponseToMessage);

VoiceChat.addEventListener('click', RecordVoice);



btn.onclick = function () {
  modal.style.display = 'block';
  btn.style.display = 'none';
};

close1.onclick = function () {
  modal.style.display = 'none';
  btn.style.display = 'block';
};

close2.onclick = function () {
  modalMain.style.display = 'none';
  btn.style.display = 'block';
};

close3.onclick = function () {
  modalQuestion.style.display = 'none';
  btn.style.display = 'block';
};

getStart.onclick = function () {
  modal.style.display = 'none';
  modalMain.style.display = 'block';
};

question.onclick = function () {
  modalMain.style.display = 'none';
  modalQuestion.style.display = 'block';
};


modal.style.display = 'block';
btn.style.display = 'none';