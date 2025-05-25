let mediaRecorder;
let audioChunks = [];
let cart = [];

function updateCart(orders) {
    const cartList = document.getElementById('cartItems');
    cartList.innerHTML = '';
    orders.forEach(order => {
        if (order.intent === 'add' && order.item !== 'invalid item') {
            cart.push(order);
        } else if (order.intent === 'remove' && order.item) {
            cart = cart.filter(item => item.item !== order.item);
        } else if (order.intent === 'confirm') {
            cart = [];
        }
    });
    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.quantity} ${item.item}, ${item.customization || 'no customization'} ($${item.price.toFixed(2)})`;
        cartList.appendChild(li);
    });
}

document.getElementById('recordButton').addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        mediaRecorder.start();
        document.getElementById('recordButton').disabled = true;
        document.getElementById('stopButton').disabled = false;
        document.getElementById('transcription').textContent = 'Transcription: Recording...';
    } catch (err) {
        console.error('Microphone access denied or unavailable:', err);
        alert('Please allow microphone access to record your order.');
        document.getElementById('transcription').textContent = 'Transcription: Microphone access denied';
    }
});

document.getElementById('stopButton').addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        document.getElementById('recordButton').disabled = false;
        document.getElementById('stopButton').disabled = true;
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recorded_audio.wav');
            formData.append('language', document.getElementById('language').value);
            try {
                const response = await fetch('/order', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                document.getElementById('transcription').textContent = `Transcription: ${result.transcription || 'unknown'}`;
                document.getElementById('order').textContent = `Order: ${result.response}`;
                document.getElementById('emotion').textContent = `Emotion: ${result.emotion}`;
                document.getElementById('confirmation').textContent = `Confirmation: ${result.confirmation_prompt}`;
                if (result.confirmation_prompt) {
                    const utterance = new SpeechSynthesisUtterance(result.confirmation_prompt);
                    utterance.lang = result.language === 'es' ? 'es-ES' : 'en-US';
                    speechSynthesis.speak(utterance);
                }
                updateCart(result.orders || []);
                fetch('/history').then(res => res.json()).then(data => {
                    const historyList = document.getElementById('orderHistory');
                    historyList.innerHTML = '';
                    data.forEach(order => {
                        const li = document.createElement('li');
                        li.textContent = `${order.language.toUpperCase()}: ${order.order} (Emotion: ${order.emotion})`;
                        historyList.appendChild(li);
                    });
                });
            } catch (err) {
                console.error('Error processing voice order:', err);
                document.getElementById('transcription').textContent = 'Transcription: Error processing order';
            }
        };
    }
});

document.getElementById('searchButton').addEventListener('click', async () => {
    const text = document.getElementById('searchInput').value;
    if (!text) {
        alert('Please enter an order in the search bar.');
        return;
    }
    const formData = new FormData();
    formData.append('text', text);
    formData.append('language', document.getElementById('language').value);
    try {
        const response = await fetch('/order', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        document.getElementById('transcription').textContent = `Transcription: ${result.transcription || 'unknown'}`;
        document.getElementById('order').textContent = `Order: ${result.response}`;
        document.getElementById('emotion').textContent = `Emotion: ${result.emotion}`;
        document.getElementById('confirmation').textContent = `Confirmation: ${result.confirmation_prompt}`;
        if (result.confirmation_prompt) {
            const utterance = new SpeechSynthesisUtterance(result.confirmation_prompt);
            utterance.lang = result.language === 'es' ? 'es-ES' : 'en-US';
            speechSynthesis.speak(utterance);
        }
        updateCart(result.orders || []);
        fetch('/history').then(res => res.json()).then(data => {
            const historyList = document.getElementById('orderHistory');
            historyList.innerHTML = '';
            data.forEach(order => {
                const li = document.createElement('li');
                li.textContent = `${order.language.toUpperCase()}: ${order.order} (Emotion: ${order.emotion})`;
                historyList.appendChild(li);
            });
        });
        document.getElementById('searchInput').value = ''; // Clear search bar
    } catch (err) {
        console.error('Error processing search order:', err);
        document.getElementById('transcription').textContent = 'Transcription: Error processing order';
    }
});