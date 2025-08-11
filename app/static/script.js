let client_session;
const prompt_textarea = document.getElementById('prompt-textarea');
const chat_container = document.getElementById('chat-container'); 

load();

async function load() {
    await get_session();
    if (client_session == undefined) {
        console.log('undefined!!');
    }
    else {
        console.log(`session: ${client_session}`);
    }

    prompt_textarea.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            await prompt_submit();
        }
    });
}

async function get_session() {
    try {
        const response = await fetch(`${url}/api/make-session`);
        const data = await response.json();
        client_session = data.session;
    }
    catch (error) {
        console.log('뭐야 이거 왜이래', error);
    }
}

async function prompt_submit() {
    try {
        const content = prompt_textarea.value;
        prompt_textarea.value = "";
        await make_chatbox_user(content);
        let assistant_chat = await make_chatbox_assistant('기다리는 중...');
        const response = await fetch(`${url}/api/enter-prompt`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session: client_session,
                prompt: content
            })
        });
        const data = await response.json();
        console.log('send',content);
        console.log('i get', data);
        
        assistant_chat.innerHTML = data['result_text'];
    }
    catch (error) {
        console.log(error);
        assistant_chat.innerHTML = '무언가 요류가 발생했습니다.';
    }
}

// async function make_chatbox(content) {
//     const newElement = document.createElement('div');
//     newElement.setAttribute('class', 'chatblock test');
//     newElement.innerHTML = `
//         <img src='static/fabicon.png'>
//         <div>
//             ${content}
//         </div>
//     `;
//     chat_container.appendChild(newElement);
// }

async function make_chatbox_assistant(content) {
    const newElement = document.createElement('div');
    newElement.setAttribute('class', 'chatblock colored');
    newElement.innerHTML = `
        <img src='static/fabicon.png'>
        <div>
            ${content}
        </div>
    `;
    chat_container.appendChild(newElement);
    return newElement.querySelector('div'); // 내부에 있는 div를 찾아서 반환22

}

async function make_chatbox_user(content) {
    const newElement = document.createElement('div');
    newElement.setAttribute('class', 'chatblock colored');
    newElement.innerHTML = `
        <h6>YOU</h6>
        <div>
            ${content}
        </div>
    `;
    chat_container.appendChild(newElement);
    return newElement.querySelector('div'); // 내부에 있는 div를 찾아서 반환
}

async function test_chatbox() {
    
}
