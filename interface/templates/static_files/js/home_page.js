window.addEventListener("scroll", getRevealed)

const reveals = document.querySelectorAll(".reveal")
const revealHeight = window.innerHeight - 150

getPersonalData().then((personalInformation) =>{
    if(personalInformation["username"] == ""){
        document.querySelector(".getstarted-btn").classList.remove("d-none")
    }else{
        document.querySelector(".submit-btn").classList.remove("d-none")
    }
})

function getRevealed(){
    for(i=0; i<reveals.length; i++){
        var reveal = reveals[i]
        var height = reveal.getBoundingClientRect().top
        if(height <= revealHeight){
            reveal.classList.add("active")
        }
    }
}
