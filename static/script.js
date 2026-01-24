document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatBox = document.getElementById('chat-box');

    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'bot' ? 'bot-message' : 'user-message');

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');

        // Check for JSON-like content
        if (text.trim().startsWith('{') && (text.includes('}') || text.includes('✅'))) {
            // Simple detection for mixed content (JSON + Confirmation text)
            // We wrap the JSON part in <pre>
            const jsonMatch = text.match(/(\{[\s\S]*\})/);
            if (jsonMatch) {
                const jsonPart = jsonMatch[0];
                const restPart = text.replace(jsonPart, '');
                contentDiv.innerHTML = `<pre>${jsonPart}</pre><br>${restPart.replace(/\n/g, '<br>')}`;
                contentDiv.classList.add('json-content');
            } else {
                contentDiv.innerHTML = text.replace(/\n/g, '<br>');
            }
        } else {
            // Convert newlines to breaks
            // Detect Links
            let formatted = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" style="color: #acf;">$1</a>');
            formatted = formatted.replace(/\n/g, '<br>');
            contentDiv.innerHTML = formatted;
        }

        messageDiv.appendChild(contentDiv);
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage(text = null) {
        const messageText = text || userInput.value.trim();
        if (messageText === "" && !text) return;

        if (!text && messageText !== "MENU_INIT") {
            appendMessage('user', messageText);
            userInput.value = '';
        }

        try {
            const formData = new URLSearchParams();
            formData.append('message', messageText);

            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                appendMessage('bot', data.reply);
            } else {
                appendMessage('bot', '⚠️ Error de conexión.');
            }
        } catch (error) {
            console.error(error);
            appendMessage('bot', '⚠️ Error técnico.');
        }
    }

    // Trigger Initial Menu
    sendMessage("MENU_INIT");

    sendBtn.addEventListener('click', () => sendMessage());

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
