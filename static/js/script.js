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

    let assistantMsg = null;
    let assistantBubble = null;
    let assistantAdded = false;
    const toolMessages = [];

    try {
        const res = await fetch('/chat/stream', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({sessionId, query})
        });

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let fullText = '';

        const empty = messagesDiv.querySelector('.empty-state');
        if (empty) empty.remove();

        assistantMsg = document.createElement('div');
        assistantMsg.className = 'message assistant';

        const meta = document.createElement('div');
        meta.className = 'msg-meta';
        meta.textContent = 'Booking Agent';

        assistantBubble = document.createElement('div');
        assistantBubble.className = 'msg-bubble';

        assistantMsg.appendChild(meta);
        assistantMsg.appendChild(assistantBubble);

        while (true) {
            const {done, value} = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    let text = line.slice(6);

                    if (text.startsWith('[') && (text.includes('Calling tool') || text.includes('Tool result'))) {
                        const toolMsg = document.createElement('div');
                        toolMsg.className = 'tool-message';
                        toolMsg.textContent = text;

                        if (assistantAdded) {
                            messagesDiv.insertBefore(toolMsg, assistantMsg);
                        } else {
                            toolMessages.push(toolMsg);
                            messagesDiv.appendChild(toolMsg);
                        }
                        messagesDiv.scrollTop = messagesDiv.scrollHeight;
                        continue;
                    }

                    if (text) {
                        if (text.startsWith('[{') || text.startsWith('["')) {
                            try {
                                const p = JSON.parse(text);
                                if (Array.isArray(p) && p[0]?.type === 'text') {
                                    text = p[0].text;
                                }
                            } catch {}
                        }

                        if (!assistantAdded) {
                            loadingDiv.classList.remove('active');
                            messagesDiv.appendChild(assistantMsg);
                            assistantAdded = true;
                        }

                        fullText += text.replace(/\\n/g, '\n');
                        assistantBubble.textContent = fullText;
                        messagesDiv.scrollTop = messagesDiv.scrollHeight;
                    }
                }
            }
        }

        if (!assistantAdded && fullText === '') {
            messagesDiv.appendChild(assistantMsg);
        }

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