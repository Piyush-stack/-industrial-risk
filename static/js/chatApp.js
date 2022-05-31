ROOT_URL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port
document.getElementById("send_btn").addEventListener("click", send_message);

let send_btn = document.getElementById('msg_inp');
send_btn.addEventListener('keyup', function(e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        document.getElementById("send_btn").click();
    }
});
async function send_message() {
    let msg = document.getElementById("msg_inp").value;
    document.getElementById('msg_inp').value = ''; //clear the text field
    chat_service_running().then(
        resp => {
            if (resp === true) {
                add_outgoing_msg_to_chat_log(msg)
                Promise.resolve(send_msg_to_bot(msg))
                    .then((response) => {
                            add_incoming_msg_to_chat_log(response)
                        },
                        (reject) => { console.log("Error sending message to bot") }
                    )
            }
        })







}

function getCurrentTime() {
    let today = new Date();
    let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    return time;
}

function add_incoming_msg_to_chat_log(response) {
    chat_log = document.getElementById("chat_log");

    let outer_div = document.createElement("div");
    chat_log.appendChild(outer_div);
    outer_div.className = "incoming_msg";
    msg_img_div = document.createElement("div");

    outer_div.appendChild(msg_img_div);
    msg_img_div.className = "incoming_msg_img";

    img_elmt = document.createElement("img");
    msg_img_div.appendChild(img_elmt);
    img_elmt.setAttribute("src", "static/blu.gif");

    rcvd_msg_elmt = document.createElement("div");
    outer_div.appendChild(rcvd_msg_elmt)
    rcvd_msg_elmt.className = "received_msg";

    text_msg_div = document.createElement("div");
    rcvd_msg_elmt.appendChild(text_msg_div)
    text_msg_div.className = "received_withd_msg";
    text_elmt = document.createElement("p");
    text_msg_div.appendChild(text_elmt);
    text_elmt.innerHTML = response;
    time_span = document.createElement("span");
    text_msg_div.appendChild(time_span)
    time_span.className = "time_date";
    time_span.innerHTML = getCurrentTime();
}

function add_outgoing_msg_to_chat_log(msg) {
    console.log("[TODO] Add message to chat log" + msg);

    let outer_div = document.createElement("div");
    outer_div.className = "outgoing_msg";

    chat_log = document.getElementById("chat_log");
    chat_log.appendChild(outer_div);
    sent_msg_elmt = document.createElement("div");
    outer_div.appendChild(sent_msg_elmt)
    sent_msg_elmt.className = "sent_msg";
    text_elmt = document.createElement("p");
    text_elmt.innerHTML = msg;
    sent_msg_elmt.appendChild(text_elmt);
    time_span = document.createElement("span");
    sent_msg_elmt.appendChild(time_span);
    time_span.className = "time_date";
    time_span.innerHTML = getCurrentTime();
}

async function send_msg_to_bot(msg) {
    msgJSON = { "text": msg }
    let resp = await postData(ROOT_URL + "/predict", msgJSON).then(
        response => {
            console.log("Msg from Bot:" + response.prediction);
            //add_outgoing_msg_to_chat_log(response.prediction);
            return response.prediction;
        },
        err => {
            console.err("Bot spoke in binary and I cannot yet speak that !!")
        }
    );
    return resp;
}

function add_message_to_chat_log(msg) {
    console.log("[TODO] Add to chat log" + msg);
}

async function chat_service_running() {
    let isAlive_url = ROOT_URL + "/isalive";
    let resp = await do_get_fetch(isAlive_url).then(
        response => {
            if (typeof(response) !== 'undefined' && response != null) {
                if (response.status === "Live") {
                    console.log('Service is live')
                    return true;
                }
            }
        },
        err => {
            console.err("Error checking service availability");
            return false;
        }
    )
    return resp;


}

function do_get_req(url, callback) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", url, true); // true for asynchronous 
    xmlHttp.send(null);
}

async function do_get_fetch(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (err) {
        console.log('fetch failed', err);
    }
}

function do_post_req(text, url) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        text: value
    }));
}

async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'same-origin', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json'
                // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    return response.json(); // parses JSON response into native JavaScript objects
}