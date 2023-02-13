var dmp = diff_match_patch;

let serverURL;
serverURL = "http://127.0.0.1:5000/"

var content; 
let slider = document.getElementById("player");
let contentDisplay = document.getElementById("displayContent");

var prettyContent = [];

function createPrettyDisplay() {
    prettyContent.push(content[0][2]);
    for(let i = 1; i < content.length; i++) {
        diff = dmp.prototype.diff_main(content[i-1][2], content[i][2]);
        prettydiff = dmp.prototype.diff_prettyHtml(diff);
        prettyContent.push(prettydiff);
    }

    console.log(prettyContent)
}


function resetSlider() {
    slider.value = 0;
    document.getElementById('textInput').value = slider.value;
}

function decrementSlider() {
    slider.value--;
    document.getElementById('textInput').value = slider.value;

    var idx = slider.value;
    // contentDisplay.textContent = content[idx][2];
    contentDisplay.innerHTML = prettyContent[idx]
}

function incrementSlider() {
    slider.value++;
    document.getElementById('textInput').value = slider.value;

    var idx = slider.value;
    // contentDisplay.textContent = content[idx][2];
    contentDisplay.innerHTML = prettyContent[idx]
}

slider.addEventListener("input", event => {
    var idx = event.target.value;
    console.log(idx);
    // contentDisplay.textContent = content[idx][2];
    contentDisplay.innerHTML = prettyContent[idx]
})

async function generateText() {
    const response = await fetch('/create', {
        method: 'GET',
    });
    const message = await response.json();
    console.log(message); 
    console.log(message[0][2]);
    content = message;

    console.log(message.length);
    contentDisplay.textContent = content[0][2];
    slider.max = message.length-1;

    resetSlider();
    createPrettyDisplay();
}

async function retrieveProject() {
    var text = document.getElementById("projectID").value;
    const object = {projectID: text};
    fetch(serverURL + "/create", {
    mode: 'no-cors',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    method: 'POST',
    body: JSON.stringify(object),
        }, function (err, resp, body) {
            if (err) {
                console.log('Could not post writer actions.');
                console.log(err);
            }
        }
    );
}

function updateTextInput(val) {
    document.getElementById('textInput').value = val; 
}

var jsons = []

function addAnnotation() {
    // var object = new Object();
    // object.beginnningIndex = startingIndex;
    // object.endingIndex = endingIndex;
    // object.label = label;
    // object.beginningText = startingText;
    // object.endingText = endingText;
    // object.changes = changes;
    

    // const jsonObject = JSON.stringify(object);
    // jsons.push(jsonObject);
}

function generateJsonFile() {
    
}