function isAuthenticated(data){
    var submitProjectEle = document.querySelectorAll(".submit-project");
    var myProfileEle = document.querySelectorAll(".my-profile");
    var signEle = document.querySelectorAll(".sign-in");

    if(data["username"]==""){
        signEle.forEach(element => {
            element.classList.remove("d-none")
        });
    }else{
        myProfileEle.forEach(element => {
            element.firstElementChild.setAttribute("href", document.location.origin + data["profileUrl"])
            element.classList.remove("d-none");
        });
        submitProjectEle.forEach(element => {
            element.classList.remove("d-none");
        });
    }
}


function isStaffFunc(isStaff){
    if(isStaff == true){
        var reviewEle = document.querySelectorAll(".review-projects");
        reviewEle.forEach(element =>{
            element.classList.remove("d-none")
        })
    }
}



getPersonalData().then((data)=>{isAuthenticated(data);isStaffFunc(data["is_staff"]);})


function sideMenu(){
    var sideMenu = document.querySelector(".side-menu");
    var displayed = sideMenu.classList.value.split(" ").includes("active");
    if(displayed == true){
        sideMenu.classList.remove("active")
    }else if(displayed == false){
        sideMenu.classList.add("active")
    }
    
}



function search(order){
    lookup = document.querySelectorAll("#search-input")[order].value
    if(lookup){
        console.log(lookup)
        var url = searchResultUrl + `?lookup=${lookup}`
        document.location.href = url
    }

}


document.querySelector(".navbar-toggler").addEventListener("click", sideMenu)
document.querySelectorAll("#search-btn")[0].addEventListener("click", function(e){e.preventDefault();search(0)})
document.querySelectorAll("#search-btn")[1].addEventListener("click", function(e){e.preventDefault();search(1)})