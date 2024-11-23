const messagesList = document.querySelector('.messages-list');
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.input_chats');
const btnSubmit = document.querySelector('.btn-send');
 

messageForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();
    // if (message.length === 0) {
    //   return;
    // }
    alert(message);

    const messageItem = document.createElement('li');
    messageItem.classList.add('message', 'sent');
    messageItem.innerHTML = `
        <div class="message-text">
            <div class="message-sender">
                <b>You</b>
            </div>
            <div class="message-content">
                ${message}
            </div>
        </div>`;
    messagesList.appendChild(messageItem);

    messageInput.value = '';

    fetch('/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      // body: new URLSearchParams({
      //   'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      //   'message_send': message
      // })
      body: JSON.stringify({input_chat: message})
    })
      .then(response => response.json())
      .then(data => {
        const response = data.response;
        const messageItem = document.createElement('li');
        messageItem.classList.add('message', 'received');
        messageItem.innerHTML = `
        <div class="message-text">
            <div class="message-sender">
              <b>AI Chatbot</b>
            </div>
            <div class="message-content">
                ${response}
            </div>
        </div>
          `;
        messagesList.appendChild(messageItem);
      });
  });
