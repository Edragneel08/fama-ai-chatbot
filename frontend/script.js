window.onload = function(){

    let oldChat = localStorage.getItem("fama_chat");

    if(oldChat){

        document.getElementById("chat-box").innerHTML = oldChat;

    }

}

async function sendMessage(){

    let input = document.getElementById("question");

    let question = input.value.trim();


    if(question === ""){
        return;
    }


    let chatBox = document.getElementById("chat-box");


    chatBox.innerHTML += `
    <div class="message user">
        ${question}
    </div>
    `;

    saveChat();

    input.value="";


    chatBox.innerHTML += `
    <div class="message bot" id="loading">
        FAMA AI sedang menaip...
    </div>
    `;


    chatBox.scrollTop = chatBox.scrollHeight;


    // delay supaya nampak AI sedang menaip
    // await new Promise(resolve => setTimeout(resolve, 1500));


    let data;

    try {

        let response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method:"POST",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify({
                    question:question
                })
            }
        );


        data = await response.json();


    }
    catch(error){

        data = {
            answer:"Maaf, sistem FAMA AI tidak dapat dihubungi."
        };

    }


    let loading = document.getElementById("loading");

    if(loading){
        loading.remove();
    }


    // chatBox.innerHTML += `
    // <div class="message bot">
    //     ${data.answer}
    // </div>
    // `;

    chatBox.innerHTML += `
    <div class="message bot">
        ${marked.parse(data.answer)}
    </div>
    `;

    saveChat();

    chatBox.scrollTop = chatBox.scrollHeight;

}


function handleEnter(event){

    if(event.key === "Enter"){
        sendMessage();
    }

}

function saveChat(){

    let chatBox = document.getElementById("chat-box");

    localStorage.setItem(
        "fama_chat",
        chatBox.innerHTML
    );

}

function clearChat(){

    localStorage.removeItem("fama_chat");

    document.getElementById("chat-box").innerHTML = "";

}