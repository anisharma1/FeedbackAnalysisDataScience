const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const outputDiv = document.getElementById('output');
const recognition = new webkitSpeechRecognition() || new SpeechRecognition();

recognition.interimResults = true;
recognition.continuous = true;

startButton.addEventListener('click', () => {
    recognition.start();
    startButton.disabled = true;
    stopButton.disabled = false;
    startButton.textContent = 'Recording...';
});

stopButton.addEventListener('click', () => {
    recognition.stop();
    startButton.disabled = false;
    stopButton.disabled = true;
    startButton.textContent = 'Start Recording';
});

recognition.onresult = event => {
    const result = event.results[event.results.length - 1][0].transcript;
    console.log(result);
    outputDiv.textContent = result;
};

recognition.onend = () => {
    startButton.disabled = false;
    stopButton.disabled = true;
    startButton.textContent = 'Start Recording';
};

recognition.onerror = event => {
    console.error('Speech recognition error:', event.error);
};

recognition.onnomatch = () => {
    console.log('No speech was recognized.');
};
