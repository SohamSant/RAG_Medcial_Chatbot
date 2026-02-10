document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatWindow = document.getElementById('chat-window');
    const promptInput = document.getElementById('prompt-input');
    const typingIndicator = document.getElementById('typing-indicator');
    const errorBanner = document.getElementById('error-banner');

    const scrollToBottom = () => {
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };

    const appendMessage = (role, content) => {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        msgDiv.innerHTML = content.replace(/\n/g, '<br>');
        chatWindow.appendChild(msgDiv);
        scrollToBottom();
    };

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const prompt = promptInput.value.trim();
        if (!prompt) return;

        // Clear input and show user message
        promptInput.value = '';
        appendMessage('user', prompt);

        // Show typing indicator
        typingIndicator.style.display = 'block';
        errorBanner.style.display = 'none';
        scrollToBottom();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            const data = await response.json();

            if (response.ok) {
                appendMessage('assistant', data.content);
            } else {
                throw new Error(data.error || 'Something went wrong');
            }
        } catch (error) {
            console.error('Error:', error);
            errorBanner.textContent = `Error: ${error.message}`;
            errorBanner.style.display = 'block';
        } finally {
            typingIndicator.style.display = 'none';
            scrollToBottom();
        }
    });

    // Submit on Enter (without Shift)
    promptInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Initial scroll
    scrollToBottom();
});
