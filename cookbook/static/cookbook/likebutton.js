//Reference for selecting multiple elements

//var elms = document.querySelectorAll("[id='duplicateID']");

//for(var i = 0; i < elms.length; i++) 
//elms[i].style.display='none'; // <-- whatever you need to do here.

document.addEventListener('DOMContentLoaded', function() {
    handlelikebuttons()
})

function getCookie(name) {
    if (!document.cookie) {
    return null;
    }
    const token = document.cookie.split(';')
    .map(c => c.trim())
    .filter(c => c.startsWith(name + '='));

    if (token.length === 0) {
    return null;
    }
    return decodeURIComponent(token[0].split('=')[1]);
}

async function handlelikebuttons() {
    var recipeIDList = document.querySelectorAll(".recipeID");
    for(var i=0;i<recipeIDList.length;i++){
        var currentID = recipeIDList[i].innerHTML;
        console.log(`ID is ${currentID}`)
        var likebutton = document.querySelector(`#like${currentID}`);
        console.log(likebutton)
        curUsername = document.querySelector("#username").textContent;
        console.log(curUsername)

        let response = await fetch(`/getrecipe/${currentID}`)
        let recipe = await response.json()
        console.log(recipe)
        likes = recipe.liked_by.length;
        if(recipe.liked_by.includes(curUsername)){
            console.log('included')
            likebutton.className = "btn btn-danger likebutton";
        } else {
            console.log('not included')
            likebutton.className = "btn btn-outline-danger likebutton";
        }
        likebutton.innerHTML = `❤️ ${likes}`

        likebutton.addEventListener('click', function() {
            postid = this.id.slice(4)
            const csrftoken = getCookie('csrftoken')
            fetch(`/getrecipe/${postid}`,{
                credentials: 'include',
                method: 'PUT',
                mode: 'same-origin',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body:JSON.stringify({
                    like: true
                })
            })
            .then(response => response.json())//Uncaught (in promise) SyntaxError: Unexpected end of JSON input
            .then(response => {
                action = response.message.slice(13);
                var likeCount = parseInt(this.textContent.slice(2))
                if(action == "Liked"){
                    this.textContent = `❤️ ${likeCount + 1}`
                    this.className = "btn btn-danger likebutton";
                } else if(action == "Unliked"){
                    this.textContent = `❤️ ${likeCount - 1}`
                    this.className = "btn btn-outline-danger likebutton";
                }
            })
        })
    }
}