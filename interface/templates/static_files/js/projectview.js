var projectData;

async function getProject(){
    var response = await fetch(projectDataUrl)
    var data = await response.json()
    return data
}

getProject().then((data)=>{
    projectData = data
    loadData()
    loadProjectPdf()
    loadReviewPdf()
})

document.querySelector("#download-project").setAttribute("href", downloadProjectUrl)
document.querySelector("#download-review").setAttribute("href", downloadReviewUrl)

function loadData(){
    if(projectData["review"]["accepted"] == true){
        var stateColor = "text-success"
        var state = "accepted"
    }else if(projectData["review"]["accepted"] == false){
        var stateColor = "text-danger"
        var state = "rejected"
    }
    document.querySelector(".assignment-date").innerText = projectData["assignment_date"]
    document.querySelector(".accepted").innerText = state
    document.querySelector(".accepted").classList.add(stateColor)
    document.querySelector(".publisher").innerText = projectData["publisher_username"]
    document.querySelector(".profile-link").setAttribute("href", projectData["profile_url"])
    document.querySelector(".description").innerText = projectData["description"]
}


//project pdf render


function loadProjectPdf(){
    var pdfLoading=pdfjsLib.getDocument(projectData["project_file"])
    pdfLoading.promise.then((pdfDocument)=>{
    projectPdf = pdfDocument
    displayProjectPage(projectPageNumber, projectPdf)
    }).catch((error)=>console.error(error))
}


function displayProjectPage(projectPageNumber, projectPdf){
    projectPdf.getPage(projectPageNumber).then((page)=>{
        var viewport = page.getViewport({scale})
        var context = projectCanvas.getContext('2d')
        projectCanvas.height = viewport.height
        projectCanvas.width = viewport.width
        
        page.render({
            canvasContext:context,
            viewport:viewport,
        })
    })
}


var projectCanvas = document.querySelector("#project-canvas")
const scale = 1.5

var projectPdf
var projectPageNumber = 1


function projectNextPage(){
    if(projectPageNumber < projectPdf.numPages){
        projectPageNumber++
        displayProjectPage(projectPageNumber, projectPdf)
    }
    return;
}


function projectPreviousPage(){
    if(projectPageNumber > 1){
        projectPageNumber--
        displayProjectPage(projectPageNumber, projectPdf)
    }
    return;
}

document.querySelector("#view-project-btn").addEventListener("click", ()=>{
    document.querySelector("#project-popup").classList.remove("d-none")
})
document.querySelector("#project-next-btn").addEventListener("click", projectNextPage)
document.querySelector("#project-prev-btn").addEventListener("click", projectPreviousPage)
document.querySelector("#close-popup-project").addEventListener("click", (e)=>{
    e.preventDefault()
    document.querySelector("#project-popup").classList.add("d-none")
})



//review pdf render


function loadReviewPdf(){
    var pdfLoading=pdfjsLib.getDocument(projectData["review"]["review_pdf"])
    pdfLoading.promise.then((pdfDocument)=>{
    reviewPdf = pdfDocument
    displayReviewPage(reviewPageNumber, reviewPdf)
    }).catch((error)=>console.error(error))
}


function displayReviewPage(reviewPageNumber, reviewPdf){
    reviewPdf.getPage(reviewPageNumber).then((page)=>{
        var viewport = page.getViewport({scale})
        var context = reviewCanvas.getContext('2d')
        reviewCanvas.height = viewport.height
        reviewCanvas.width = viewport.width
        
        page.render({
            canvasContext:context,
            viewport:viewport,
        })
    })
}


var reviewCanvas = document.querySelector(("#review-canvas"))

var reviewPdf
var reviewPageNumber = 1


function reviewNextPage(){
    if(reviewPageNumber < reviewPdf.numPages){
        reviewPageNumber++
        displayReviewPage(reviewPageNumber, reviewPdf)
    }
    return;
}


function reviewPreviousPage(){
    if(reviewPageNumber > 1){
        reviewPageNumber--
        displayReviewPage(reviewPageNumber, reviewPdf)
    }
    return;
}

document.querySelector("#view-review-btn").addEventListener("click", ()=>{
    document.querySelector("#review-popup").classList.remove("d-none")
})
document.querySelector("#review-next-btn").addEventListener("click", reviewNextPage)
document.querySelector("#review-prev-btn").addEventListener("click", reviewPreviousPage)
document.querySelector("#close-popup-review").addEventListener("click", (e)=>{
    e.preventDefault()
    document.querySelector("#review-popup").classList.add("d-none")
})