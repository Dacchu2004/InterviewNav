document.addEventListener("DOMContentLoaded", () => {
    // Speech Recognition Code
    const startButton = document.getElementById("start-speech");
    const doneButton = document.getElementById("done");
    const transcriptionBox = document.getElementById("transcribed-response");
    const hiddenResponseInput = document.getElementById("hidden-response");

    let recognition;
    if ("webkitSpeechRecognition" in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = "en-US";

        recognition.onresult = (event) => {
            let interimTranscription = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    transcriptionBox.textContent += transcript + " ";
                } else {
                    interimTranscription += transcript;
                }
            }
            hiddenResponseInput.value = transcriptionBox.textContent + interimTranscription;
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error);
        };
    } else {
        console.warn("Speech recognition not supported in this browser.");
    }

    startButton.addEventListener("click", () => {
        if (recognition) {
            transcriptionBox.textContent = ""; // Clear previous transcription
            hiddenResponseInput.value = ""; // Clear hidden input
            recognition.start();
        } else {
            alert("Speech recognition is not supported in your browser.");
        }
    });

    doneButton.addEventListener("click", () => {
        if (recognition) {
            recognition.stop();
        }
    });

    // Text-to-Speech for Question
    function speakText(text) {
        const speech = new SpeechSynthesisUtterance(text);
        speech.lang = 'en-US';
        window.speechSynthesis.speak(speech);
    }

    // Automatically speak the question when it's displayed
    const questionText = document.getElementById("question-text");
    if (questionText) {
        const question = questionText.textContent || questionText.innerText;
        speakText(question);
    }

    // Form Validation for Sign-Up and Login
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const password = document.querySelector('input[name="password"]');
            const confirmPassword = document.querySelector('input[name="confirm_password"]');
            
            if (password && confirmPassword && password.value !== confirmPassword.value) {
                alert("Passwords do not match!");
                event.preventDefault();
            }
        });
    }

    // Smooth Scrolling for Internal Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Interactive Hover Effect for Buttons
    const buttons = document.querySelectorAll('.submit');
    buttons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.style.backgroundColor = '#2980b9';
        });
        button.addEventListener('mouseout', function() {
            this.style.backgroundColor = '#3498db';
        });
    });
});
