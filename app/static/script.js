let client_session;

load();

async function load() {
    await get_session();
    if (client_session == undefined) {
        console.log('undefined!!');
    }
    else {
        console.log(`session: ${client_session}`);
    }
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
        const content = document.getElementById('prompt-textarea').value;
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
        console.log('i get', data)
    }
    catch (error) {
        console.log(error);
    }
}
