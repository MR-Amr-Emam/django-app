const loadingScreen = document.querySelector("#loading-screen")

function submit(e){
    e.preventDefault()
    document.querySelector(".file-error-1").classList.add("d-none")
    document.querySelector(".file-error-2").classList.add("d-none")
    document.querySelector(".description-error").classList.add("d-none")
    const projectDescription = document.getElementById("project_description").value
    const projectFile = document.getElementById("project_file").files[0]
    const formData = new FormData()

    if(projectFile==undefined){
        document.querySelector(".file-error-1").classList.remove("d-none")
        return;
    }
    if(projectFile["name"].slice(projectFile["name"].lastIndexOf(".")+1)!="pdf"){
        document.querySelector(".file-error-2").classList.remove("d-none") 
        return;
    }
    if(projectDescription==""){
        document.querySelector(".description-error").classList.remove("d-none")
        return;
    }

    loadingScreen.classList.remove("d-none")

    formData.append("project_file", projectFile)
    formData.append("description", projectDescription)

    async function sendingData(){       

        response = await fetch(projectUrl, {
            method:"POST",
            headers:{
                'X-CSRFToken': csrftoken,
            },
            body: formData,
        })

        return await response.json()
    }

    sendingData().then(data =>{
        loadingScreen.classList.add("d-none")
        document.querySelector(".popup").classList.remove("d-none")
    })

}


document.querySelector(".btn-warning").addEventListener("click", submit)
document.querySelector(".close-btn").addEventListener("click", ()=>{
    document.querySelector(".popup").classList.add("d-none")
    document.location.href = document.location.origin + homepageUrl
})