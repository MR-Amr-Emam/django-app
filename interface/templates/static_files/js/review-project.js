async function getProjectData(){
    const projectData = {}
    var data = await fetch(projectURL, {
        method:"GET",
        })
    
    var data = await data.json()
    
    projectData["id"] = data["id"]
    projectData["pdfurl"] = data["project_file"]
    projectData["description"] = data["description"]
    projectData["publisher_id"] = data["publisher"]
    projectData["publisher_username"] = data["publisher_username"]
    projectData["assignment_date"] = data["assignment_date"]

    return projectData
}


function loadPdf(projectData){
    const pdfLoading=pdfjsLib.getDocument(projectData["pdfurl"])
    pdfLoading.promise.then((pdfDocument)=>{
    pdf = pdfDocument
    displayPage(pageNumber, pdf)
    }).catch((error)=>console.error(error))
}


function displayPage(pageNumber, pdf){
    pdf.getPage(pageNumber).then((page)=>{
        var viewport = page.getViewport({scale})
        var context = canvas.getContext('2d')
        canvas.height = viewport.height
        canvas.width = viewport.width
    
        page.render({
            canvasContext:context,
            viewport:viewport,
        })
    })
}


var canvas = document.querySelector((".pdf-canvas"))
const scale = 1.5

var pdf = null
var pageNumber = 1


function nextPage(){
    if(pageNumber < pdf.numPages){
        pageNumber++
        displayPage(pageNumber, pdf)
    }
    return;
}


function previousPage(){
    if(pageNumber > 1){
        pageNumber--
        displayPage(pageNumber, pdf)
    }
    return;
}

function closePopupProject(e){
    e.preventDefault();
    document.querySelector("#popup-project").style.display = "none";
}

function viewProject(e){
    e.preventDefault();
    document.querySelector("#popup-project").style.display = "block";
}


document.querySelector(".next-btn").addEventListener("click", nextPage)
document.querySelector(".previous-btn").addEventListener("click", previousPage)
document.querySelector(".close-project-btn").addEventListener("click", closePopupProject)
document.querySelector(".view-project").addEventListener("click", viewProject)


function displayData(reviewProject){
    document.querySelector(".project_assignment_date").innerText = reviewProject["assignment_date"];
    document.querySelector(".project_publisher").innerText = reviewProject["publisher_username"];
    document.querySelector(".project_description").innerText = reviewProject["description"];
}


getProjectData().then((data)=>{loadPdf(data);displayData(data)})


async function getReviewData(){
    const reviewData = {}
    var data = await fetch(reviewURL, {
        method:"GET",
    })

    var data = await data.json()

    reviewData["id"] = data["id"]
    return reviewData
}

var reviewData;
getReviewData().then(data => reviewData=data)




const cropperBuilt = document.querySelector(".cropper-container-built")

var cropper;
document.querySelector("#get-cropper").addEventListener("click", ()=>{

    try{document.querySelector(".cropper-comment-image-container").remove()}catch{}

    var canvas = document.querySelector((".pdf-canvas"))
    document.querySelector("#popup-project").style.display = "none";
    cropperBuilt.classList.add("active")


    document.querySelector(".cropper-image-container").innerHTML = 
    "<div class='cropper-comment-image-container w-100'>"
    +   "<img class='cropper-comment-image w-100'>"
    +"</div>"

    cropperImage=document.querySelector(".cropper-comment-image")
    cropperImage.src = canvas.toDataURL("image/jpeg")


    cropper = new Cropper(cropperImage, {
        zoomable:false,
        ready() {
            croppable = true;
        },
    });
})


function sendComment(){
    var croppedCanvas = cropper.getCroppedCanvas()
    var formData = new FormData()
    croppedCanvas.toBlob((blob)=>{
        var commentImage = new File([blob], `comment_review_${reviewData["id"]}.jpg`)
                
        formData.append("image_comment", commentImage)
        formData.append("rate", document.querySelector("#rate").value)
        formData.append("comment", document.querySelector("#text-comment").value)
        formData.append("review_id", reviewData["id"])

        if(formData.get("comment") == false){
            document.querySelector(".warn-comment-message").classList.remove("d-none")
        }else{
            fetch(commentURL, {
                method: "POST",
                headers:{
                    "X-CSRFToken":csrftoken,
                },
                body: formData,
            })

            document.querySelector(".warn-comment-message").classList.add("d-none")
            cropperBuilt.classList.remove("active")
            document.querySelector("#popup-project").style.display = "block";
        }
    })
}


document.querySelector(".comment-btn").addEventListener("click", sendComment)


document.querySelector(".close-cropper-btn").addEventListener("click", (e)=>{
    e.preventDefault()
    cropperBuilt.classList.remove("active")
})



function submitReview(value){

    document.querySelector("#popup-review").style.display = "block"

    var generalComment = document.querySelector("#general-comment").value
    var rate = document.querySelector("#general-rate").value

    if(generalComment==false){
        document.querySelector(".warn-general-comment-message").classList.remove("d-none")
        return;
    }
    document.querySelector(".warn-general-comment-message").classList.add("d-none")

    var bodyOne = JSON.stringify({
        "rate": rate,
        "comment": generalComment,
        "general_comment": "True",
        "review_id":reviewData["id"],
    })

    async function sendGeneralComment(){
        var response = await fetch(commentURL, {
            method:"POST",
            headers:{
                "X-CSRFToken":csrftoken,
                "Content-Type":"application/json",
            },
            body:bodyOne,
        })

        data = await response.json()
        return data
    }
           
    finishReviewURL = finishReviewURL.replace("555", reviewData["id"])
    var bodyTwo = JSON.stringify({
        "accepted":value,
    })

    async function sendReview(){
        var response = await fetch(finishReviewURL, {
            method:"PUT",
            headers:{
                "X-CSRFToken":csrftoken,
                "Content-Type":"application/json",
            },
            body:bodyTwo,
        })

        var data = await response.json()
        return data
    }
    sendGeneralComment().then(data=>{sendReview().then(data=>{getReviewPdf(document.location.origin + data["review_pdf"])})})

}

function getReviewPdf(reviewUrl){
    function loadPdf(reviewUrl){
        const reviewPdfLoading=pdfjsLib.getDocument(reviewUrl)
        reviewPdfLoading.promise.then((reviewPdf)=>{
        pdf = reviewPdf
        displayPage(pageNumber, pdf)
        document.querySelector("#review-loading-screen").classList.add("d-none")
        document.querySelector("#review-container").classList.remove("d-none")
        }).catch((error)=>console.error(error))
    }
    
    
    function displayPage(pageNumber, pdf){
        pdf.getPage(pageNumber).then((page)=>{
            var viewport = page.getViewport({scale})
            var context = canvas.getContext('2d')
            canvas.height = viewport.height
            canvas.width = viewport.width
        
            page.render({
                canvasContext:context,
                viewport:viewport,
            })
        })
    }
    
    
    var canvas = document.querySelector(("#review-pdf"))
    const scale = 1.5
    
    var pdf = null
    var pageNumber = 1
    
    
    function reviewPdfNextPage(){
        if(pageNumber < pdf.numPages){
            pageNumber++
            displayPage(pageNumber, pdf)
        }
        return;
    }
    
    
    function reviewPdfPreviousPage(){
        if(pageNumber > 1){
            pageNumber--
            displayPage(pageNumber, pdf)
        }
        return;
    }

    loadPdf(reviewUrl)
    document.querySelector("#review-pdf-next-btn").addEventListener("click", reviewPdfNextPage)
    document.querySelector("#review-pdf-prev-btn").addEventListener("click", reviewPdfPreviousPage)
}

document.querySelector("#accept-project").addEventListener("click",()=>{submitReview(true)})
document.querySelector("#reject-project").addEventListener("click",()=>{submitReview(false)})

async function completeFinsihReviewFunc(state){
    var response = await fetch(completeFinishReviewUrl, {
        method:"PUT",
        headers:{
            "X-CSRFToken":csrftoken,
            "Content-Type":"application/json",
        },
        body:JSON.stringify({
            "state":state,
            "review_id":reviewData["id"],
        }),
    })
    data = await response.json()
    return data
}

document.querySelector("#review-complete-finish-review-true")
.addEventListener("click", ()=>{completeFinsihReviewFunc(true).then((data)=>{
    if(data["state"] == true){
        window.location.replace(projectsUrl)
    }
})})

document.querySelector("#review-complete-finish-review-false")
.addEventListener("click", ()=>{completeFinsihReviewFunc(false).then((data)=>{
    if(data["state"]==false){
        window.location.reload()
    }
})})