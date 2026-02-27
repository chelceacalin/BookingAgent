const sessionId = 'session_' + Date.now();
const messagesDiv = document.getElementById('messages');
const queryInput = document.getElementById('query');
const sendBtn = document.getElementById('send');
const loadingDiv = document.getElementById('loading');

function addMessage(content, role) {
    const empty = messagesDiv.querySelector('.empty-state');
    if (empty) empty.remove();

    const msg = document.createElement('div');
    msg.className = `message ${role}`;

    const meta = document.createElement('div');
    meta.className = 'msg-meta';
    meta.textContent = role === 'user' ? 'You' : 'Booking Agent';

    const bubble = document.createElement('div');
    bubble.className = 'msg-bubble';
    bubble.textContent = content;

    if (role === 'assistant') {
        msg.appendChild(meta);
        msg.appendChild(bubble);
    } else {
        msg.appendChild(bubble);
        msg.appendChild(meta);
    }

    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const query = queryInput.value.trim();
    if (!query) return;

    addMessage(query, 'user');
    queryInput.value = '';
    sendBtn.disabled = true;
    loadingDiv.classList.add('active');
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({sessionId, query})
        });
        const data = await res.json();
        let text = data.response;

        if (typeof text === 'string') {
            try {
                const p = JSON.parse(text);
                if (Array.isArray(p) && p[0]?.type === 'text') text = p[0].text;
            } catch {
            }
        }

        addMessage(text, 'assistant');
    } catch (e) {
        addMessage('Something went wrong. Please try again.', 'assistant');
    }

    sendBtn.disabled = false;
    loadingDiv.classList.remove('active');
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
queryInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') sendMessage();
});