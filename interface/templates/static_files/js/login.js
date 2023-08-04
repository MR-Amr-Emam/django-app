function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


const Btn = document.getElementsByTagName("button")[0]
const loadingScreen = document.querySelector("#loading-screen")
const container = document.querySelector(".container")

function login(e){
    e.preventDefault()


    const username = document.getElementById("floatingInput").value
    const password = document.getElementById("floatingPassword").value
    const formData = new FormData()

    container.classList.add("d-none")
    loadingScreen.classList.remove("d-none")
    formData.append("username", username)
    formData.append("password", password)
    
    async function login(){
        var response = await fetch(loginUrl, {
            method:"POST",
            headers:{
                "X-CSRFToken": csrftoken,
            },
            body:formData,
        })

        return await response.json()
    }

    login().then(response => {
        if(response["url"] != undefined){
            url = window.location.origin + response["url"]
            window.location.href = url
        }if(response["error"] != undefined){
            var p = document.getElementsByClassName("text-danger")[0]
            p.innerText = response["error"]
            document.getElementById("floatingPassword").classList.add("is-invalid")
            loadingScreen.classList.add("d-none")
            container.classList.remove("d-none")
        }
    })

}


Btn.addEventListener("click", login)