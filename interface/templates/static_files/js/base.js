function isAuthenticated(data){
    if(data["username"]==""){
        var navbar = document.querySelector(".navbar-nav");
        navbar.innerHTML += `<li class="nav-item"><a class="nav-link active"
        href="${loginUrl}">sign in</a></li>`
    }else{
        var navbar = document.querySelector(".navbar-nav");
        navbar.innerHTML += `<li class="nav-item"><a class="nav-link active"
        href="${submitUrl}">submit project</a></li>`
        navbar.innerHTML += `<li class="nav-item">
        <a class="nav-link active personalprofile" href="${data["profileUrl"]}">my profile</a></li>`;
    }
}


function isStaffFunc(isStaff){
    if(isStaff == true){
        var navbar = document.querySelector(".navbar-nav");
        navbar.innerHTML += `<li class="nav-item"><a href=${notCompleteprojectsUrl} class="nav-link active text-success fw-bold">review projects</a></li>`;
    }
}



getPersonalData().then((data)=>{isAuthenticated(data);isStaffFunc(data["is_staff"]);})


function search(e){
    e.preventDefault()
    lookup = document.querySelector("#search-input").value
    if(lookup){
        console.log(lookup)
        var url = searchResultUrl + `?lookup=${lookup}`
        document.location.href = url
    }

}

document.querySelector("#search-btn").addEventListener("click", search)
