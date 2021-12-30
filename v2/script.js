
const ip = "http://192.168.0.2:5000"


function afterResponse(response) {
    console.log(response)
}

const upload = (file) => {
    const formData = new FormData();
    formData.append("file", file);


    fetch(ip, {
        method: "POST",
        body: formData
    }).then((response) => response.text()
    ).then(
        success => afterResponse(success)
    ).catch(
        error => console.log(error)
    );

}

function getCurrentData(){


    fetch(ip /*+ "/users?" + new URLSearchParams({
            name : "alex", 
            age : 19
    })*/)
    .then(
        (response) => response.text()
    ).then(
        success => afterResponse(success)
    ).catch(
        error => console.log(error)
    );
}

function sendFile(){
    const input = document.getElementById("file-input");
    if (input.files[0]){
        
        upload(input.files[0])
    } else {
        alert("Choose file")
    }
}

