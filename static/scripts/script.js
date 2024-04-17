const startButton = document.getElementById("startButton");
const stopButton = document.getElementById("stopButton");
const outputDiv = document.getElementById("output");
const recognition = new webkitSpeechRecognition() || new SpeechRecognition();

recognition.interimResults = true;
recognition.continuous = true;

startButton.addEventListener("click", () => {
	recognition.start();
	startButton.disabled = true;
	stopButton.disabled = false;
	startButton.textContent = "Recording...";
});

stopButton.addEventListener("click", () => {
	recognition.stop();
	startButton.disabled = false;
	stopButton.disabled = true;
	startButton.textContent = "Start Recording";
});

recognition.onresult = (event) => {
	const user_input = event.results[event.results.length - 1][0].transcript;
	console.log(user_input);
	// Display user input in the userText div
	document.getElementById("userText").textContent = user_input;

	fetch("/analyze_emotion", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ text: user_input }),
	})
		.then((response) => response.json())
		.then((data) => {
			console.log(data.emotion);
			// Display user input and detected emotion in the output div
			outputDiv.textContent = `Detected Emotion: ${data.emotion}`;
		})
		.catch((error) => console.error("Error:", error));
};

recognition.onend = () => {
	startButton.disabled = false;
	stopButton.disabled = true;
	startButton.textContent = "Start Recording";
};

recognition.onerror = (event) => {
	console.error("Speech recognition error:", event.error);
};

recognition.onnomatch = () => {
	console.log("No speech was recognized.");
};
