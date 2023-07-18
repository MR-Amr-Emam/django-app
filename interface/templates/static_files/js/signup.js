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

function signup(e){

    e.preventDefault()

    var username = document.getElementById("username")
    var email = document.getElementById("email")
    var password = document.getElementById("Password")
    var confirmPassword = document.getElementById("confirm-Password")
    var formData = new FormData()

    formData.append("username", username.value)
    formData.append("email", email.value)
    formData.append("password", password.value)
    formData.append("confirm-password", confirmPassword.value)
    
    async function signup(){
        var response = await fetch(signupUrl, {
            method:"POST",
            headers:{
                "X-CSRFToken": csrftoken,
            },
            body:formData,
        })
        return await response.json()
    }

    signup().then(response => {
        if(response["result"] == "negative"){
            if(response["username"] != undefined){
                username.classList.add("is-invalid")
                document.getElementById("username-danger").innerText = response["username"]
            }else{
                username.classList.remove("is-invalid")
                document.getElementById("username-danger").innerText = ""
            }
            if(response["password"] != undefined){
                password.classList.add("is-invalid")
                document.getElementById("password-danger").innerText = response["password"]
            }else{
                username.classList.remove("is-invalid")
                document.getElementById("password-danger").innerText = ""
            }
            if(response["confirm-password"] != undefined){
                confirmPassword.classList.add("is-invalid")
                document.getElementById("confirm-password-danger").innerText = response["confirm-password"]
            }else{
                confirmPassword.classList.remove("is-invalid")
                document.getElementById("confirm-password-danger").innerText = ""
            }
        }else if(response["result"] == "positive"){
            document.location.replace(profileUrl.replace("username", response["username"])+"?new=yes")
        }
    })

}


Btn.addEventListener("click", signup)