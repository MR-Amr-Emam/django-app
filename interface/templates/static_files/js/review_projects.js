async function getAllProjects(){
    var response = await fetch(projectsUrl)
    var data = await response.json()
    return data
}

getAllProjects().then(data=>{
   var projectsContainer = document.getElementById("projects");
   var fragment = new DocumentFragment();
   var ele = document.createElement("span");
   for(let i=0; i<data.length; i++){
    ele.innerHTML += `<div class="border-top pb-3 ps-2">
                          <p class="text-success">${data[i]["assignment_date"]}</p>
                          <p>made by <span class="fw-bold"><a class="text-decoration-none text-black" href="${document.location.origin
                            +data[i]["profile_url"]}">${data[i]["publisher_username"]}</a></span></p>
                          <p>id ${data[i]["id"]}</p>
                          <p>${data[i]["description"]}</p>
                          <p><a href="${data[i]["review_project_page_url"]}">review project</a></p>
                      </div>`

   }
   fragment.appendChild(ele);
   projectsContainer.appendChild(fragment);
})