//initial loaing

fetch(userUrl, {
    method:"GET",
}).then(response => response.json()).then(data => {
    initialLoad(data);
    document.querySelector("#profile-image").addEventListener("click", openImagePopup);
    document.querySelector("#username").addEventListener("click", ()=>{userInformationPopup.classList.add("active")})
})


function initialLoad(data){

    var croppedProfileImageSrc = window.location.origin + data["user_information"]["cropped_image_url"]
    document.querySelector("#profile-image").setAttribute("src", croppedProfileImageSrc)

    var profileImageSrc = window.location.origin + data["user_information"]["profile_image_url"]
    document.querySelector(".popup-profile-image").setAttribute("src", profileImageSrc)

    document.getElementById("username").innerText = data["username"]
    document.getElementById("bio").innerText = data["user_information"]["bio"]

    //user information

    var usernameForm = document.getElementById("form-username")
    var emailForm = document.getElementById("form-email")
    var bioForm = document.getElementById("form-bio")

    usernameForm.setAttribute("value", data["username"])
    emailForm.setAttribute("value", data["email"])
    bioForm.setAttribute("value", data["user_information"]["bio"])

    if(personalInformation["username"]==data["username"]){
        document.querySelector(".logout").classList.remove("d-none")
        document.querySelector(".change-btn").classList.remove("d-none")
        document.querySelector(".change-btn").addEventListener("click",()=>{
            changeUserInformation(usernameForm, emailForm, bioForm)
        })
    }else{
        usernameForm.setAttribute("readonly", "")
        emailForm.setAttribute("readonly", "")
        bioForm.setAttribute("readonly", "")
    }


}


//constants


const profileImageEle = document.getElementById("profile-image")
const popupOverlay = document.getElementsByClassName("popup-overlay")[0]
const closeBtn = document.getElementsByClassName("close-btn")[0]
const cropBtn = document.getElementById("crop-btn")
const changeImageBtn = document.getElementById("change-image-btn")
const userInformationPopup = document.getElementsByClassName("userinformationpopup-overlay")[0]
const loadingScreen = document.getElementById("loading-screen")


//cropping

var cropper;
function openImagePopup(){

    popupOverlay.classList.add("active")

    if(personalInformation["username"]==username){

        var imageUrl = document.querySelector(".popup-profile-image").src
        try{
            document.querySelector(".image-container").remove()
        }catch{}

        document.querySelector(".image-buttons").classList.add("active")
        document.querySelector(".image-canvas-container").innerHTML =
        "<div class='image-container'>"
        +    `<img class='popup-profile-image' src='${imageUrl}'>`
        +"</div>"

        var popupProfileImage = document.querySelector(".popup-profile-image")
        cropper = new Cropper(popupProfileImage, {
            aspectRatio: 1,
            viewMode: 1,
            ready: function () {
              croppable = true;
            }
        });
    }
}

function crop(){
    loadingScreen.classList.add("active")
    if(changeImageBtn != ""){
        var image = changeImageBtn.files[0]
        var croppedCanvas = cropper.getCroppedCanvas();
        profileImageEle.src = croppedCanvas.toDataURL();
        sendImage(croppedCanvas, image).then((data)=>{
            popupOverlay.classList.remove("active");
            loadingScreen.classList.remove("active");
        })
    }else{
        croppedCanvas = cropper.getCroppedCanvas();
        profileImageEle.src = croppedCanvas.toDataURL();
        sendImage(croppedCanvas).then((data)=>{
            popupOverlay.classList.remove("active");
            loadingScreen.classList.remove("active");
        })
    }
}




//changing image


function changeImage() {
    var image = changeImageBtn.files[0]
    var imageUrl = URL.createObjectURL(image)

    document.querySelector(".image-container").remove()
    let divEle = document.createElement("div")
    divEle.setAttribute("class", "image-container")
    let imageEle = document.createElement("img")
    imageEle.setAttribute("src", imageUrl)
    imageEle.setAttribute("class", "popup-profile-image")
    divEle.appendChild(imageEle)
    let container = document.querySelector(".image-canvas-container")
    container.appendChild(divEle)

    cropper = new Cropper(imageEle, {
        aspectRatio: 1,
        viewMode: 1,
        ready: function () {
          croppable = true;
        }});
}


function getCanvasBlob(canvas) {
    return new Promise(function(resolve, reject) {
      canvas.toBlob(function(blob) {
        resolve(blob)
      })
    })
  }


async function sendImage(croppedCanvas, image=null){
    var blob = await getCanvasBlob(croppedCanvas);
    var croppedImage = new File([blob], "cropped_profile.jpg")
    var formData = new FormData()
    if(image!=null){
        formData.append("profile_image", image)
    }
    formData.append("cropped_profile_image", croppedImage)

    var response = await fetch(userInformationUrl,{
        method:"PUT",
        headers:{
            "X-CSRFToken":csrftoken,
        },
        body:formData,
    })
    return response
}


cropBtn.addEventListener("click", crop)
changeImageBtn.addEventListener("change", changeImage)


//changing user information

function changeUserInformation(usernameForm, emailForm, bioForm){
    loadingScreen.classList.add("active")
    async function sendData(){
        var response1 = await fetch(userInformationUrl, {
            method:"PUT",
            headers:{
                "X-CSRFToken":csrftoken,
                "Content-Type":"application/json",
            },
            body:JSON.stringify({"bio":bioForm.value}),
        })
        var response2 = await fetch(userUrl, {
            method:"PUT",
            headers:{
                "X-CSRFToken":csrftoken,
                "Content-Type":"application/json",
            },
            body:JSON.stringify({"username":usernameForm.value, "email":emailForm.value}),
        })
        var data = await response2.json()
        return data
    }
    sendData().then((data) => {
        document.getElementById("username").innerText = data["username"]
        document.getElementById("bio").innerText = data["user_information"]["bio"]
        usernameForm.setAttribute("value", data["username"])
        emailForm.setAttribute("value", data["email"])
        bioForm.setAttribute("value", data["user_information"]["bio"])
        userInformationPopup.classList.remove("active")
        loadingScreen.classList.remove("active")
    })
}

// close btn actions


closeBtn.addEventListener("click", ()=>{
    popupOverlay.classList.remove("active")
})

document.getElementsByClassName("userinformationpopupclose-btn")[0].addEventListener("click", ()=>{
    userInformationPopup.classList.remove("active")
})


