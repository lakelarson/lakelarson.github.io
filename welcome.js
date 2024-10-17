const texts = ["Hello", "My name is Lake Larson", "Welcome to my website :)"];
let currentTextIndex = 0;
let currentCharIndex = 0;
let deleting = false;
const typingSpeed = 30;
const deletingSpeed = 15;
const pauseBetweenTexts = 1000;


const outputElement = document.getElementById('output');
const commandPrompt = document.getElementById('commandPrompt');

function typeText() {
    // Only show the cursor on the current typing line
    let currentLine = "> " + texts[currentTextIndex].substring(0, currentCharIndex);
    if (currentCharIndex < texts[currentTextIndex].length) {
        outputElement.innerHTML = currentLine + '<span id="cursor">|</span>';
    } else {
        outputElement.innerHTML = currentLine;
    }

    if (!deleting && currentCharIndex < texts[currentTextIndex].length) {
        currentCharIndex++;
        setTimeout(typeText, typingSpeed);
    } else if (!deleting && currentCharIndex === texts[currentTextIndex].length) {
        if (currentTextIndex < texts.length - 1) {
            setTimeout(() => {
                deleting = true;
                typeText();
            }, pauseBetweenTexts);
        } else {
            document.getElementById('cursor').style.display = 'none'; // Hide cursor after last line
        }
    } else if (deleting && currentCharIndex > 0) {
        currentCharIndex--;
        setTimeout(typeText, deletingSpeed);
    } else if (deleting && currentCharIndex === 0) {
        deleting = false;
        currentTextIndex++;
        setTimeout(typeText, typingSpeed);
    }
}
window.onload = typeText;