var pagenum = 1;
var rangemin = 0;
var rangemax = 4;



function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function updatePagiNav(type) {
    var pageul = document.querySelector('.pagination');
    pageul.innerHTML = "";
    var previousbutton = document.createElement("li");
    if(pagenum - 1 == 0){
        previousbutton.className = 'page-item disabled';
        previousbutton.innerHTML = '<a class="page-link" href="#">Previous</a>';
    } else {
        previousbutton.className = 'page-item';
        previousbutton.innerHTML = '<a class="page-link" href="#">Previous</a>';
        if((pagenum-1) % 3 == 0){
            previousbutton.addEventListener('click', function() {
                pagenum = rangemin
                updateRange();
                updatePagiNav(type);
                loadPosts(type, pagenum);
            });
        } else {
            previousbutton.addEventListener('click', function() {
                pagenum -= 1;
                updatePagiNav(type);
                loadPosts(type, pagenum);
            });            
        }
    }
    pageul.appendChild(previousbutton)
    for(i = rangemin + 1; i < rangemax;i++){
        var pagebutton = document.createElement("li")
        pagebutton.id = `Page${i}`
        if(pagenum == i){
            pagebutton.className = 'page-item active';
        } else {
            pagebutton.className = 'page-item';
        }
        pagebutton.innerHTML = `<a class="page-link" href="#">${i}</a>`
        pagebutton.addEventListener('click', function() {
            pagenum = this.id.slice(4);
            updatePagiNav(type);
            loadPosts(type, pagenum);
        })
        pageul.appendChild(pagebutton);
    }
    var nextbutton = document.createElement("li")
    nextbutton.className = 'page-item';
    nextbutton.innerHTML = '<a class="page-link" href="#">Next</a>';
    if(pagenum % 3 == 0){
        nextbutton.addEventListener('click', function() {
            pagenum = rangemax;
            updateRange();
            updatePagiNav(type);
            loadPosts(type, pagenum);
        });
    } else {
        nextbutton.addEventListener('click', function() {
            pagenum += 1;
            updatePagiNav(type);
            loadPosts(type, pagenum);
        });
    }
    pageul.appendChild(nextbutton);
}

function updateRange() {
    x = pagenum;
    if(x%3 == 0){
        x -= 1;
    }
    rangemin = Math.floor((x)/3) * 3;
    rangemax = rangemin + 4;
}

function loadPosts(type, pagenum) {
    //clear out existings posts
    document.querySelector('#postContainer').innerHTML = ''

    //fetch
    fetch(`/posts/${type}/${pagenum}`)
    .then(response => response.json())
    .then(posts => {
        console.log(posts)
        if(posts.error == "No page for the given page number") {
            document.querySelector('#postContainer').style.display = 'none';
            document.querySelector('#blockError').style.display = 'block';
        } else if(posts.length == 0) {
            document.querySelector('#postContainer').style.display = 'none';
            document.querySelector('#blockError').style.display = 'block';

        } else {
            
            document.querySelector('#postContainer').style.display = 'block';
            document.querySelector('#blockError').style.display = 'none';
            container = document.querySelector('#postContainer')
            for(entry in posts) {
                curUsername = document.querySelector("#Loggedinusername").innerHTML;
                console.log(posts[entry]);
                post = posts[entry];
                likes = post.liked_by.length;
                console.log(likes);
                div = document.createElement('div');
                div.className = "card";

                if(curUsername == post.author){
                    div.innerHTML = `
                    <div class="card-body" style="margin-top:None;">
                        <a href="#" id="edit${post.id}">Edit</a>
                        <p class="card-text" id="content${post.id}">${post.content}</p>
                        <div id="editor${post.id}" style="display:none">
                            <textarea id="area${post.id}">${post.content}</textarea>
                            <a href="#" id="save${post.id}">Save</a>
                        </div>
                        <p class="card-text" style="color:grey;">by <a href="/profile/${post.author}">${post.author}</a> on ${post.timestamp}</p>
                        <a href="#" id="like${post.id}" style="margin-right:2rem;">❤️ ${likes}</a>
                    <div>`;

                    container.appendChild(div);

                    b_edit = document.querySelector(`#edit${post.id}`);
                    b_edit.addEventListener('click', function() {
                        postid = this.id.slice(4);
                        console.log(`edit clicked ${postid}`);
                        document.querySelector(`#content${postid}`).style.display = "none";
                        document.querySelector(`#editor${postid}`).style.display = "block";
                        return false;
                    })

                    b_save = document.querySelector(`#save${post.id}`);
                    b_save.addEventListener('click', function() {
                        postid = this.id.slice(4);
                        editedcontent = document.querySelector(`#area${postid}`).value
                        fetch(`/post/${postid}`, {
                            method: 'PUT',
                            body:JSON.stringify({
                                content: editedcontent
                            })
                        })
                        .then(response => response.json())//Uncaught (in promise) SyntaxError: Unexpected end of JSON input
                        .then(response => {
                            action = response.message.slice(13);
                            
                            if(action == "Edited"){
                                document.querySelector(`#content${postid}`).style.display = "block";
                                document.querySelector(`#editor${postid}`).style.display = "none";
                                document.querySelector(`#content${postid}`).innerHTML = editedcontent;
                            } else {
                                //Task failed User not authenticated
                                document.querySelector(`#area${postid}`).value = `${editedcontent} Failed To Update`
                            }
                        })
                    })

                } else {
                    div.innerHTML = `
                    <div class="card-body" style="margin-top:None;">
                        <p class="card-text" id="content${post.id}">${post.content}</p>
                        <p class="card-text" style="color:grey;">by <a href="/profile/${post.author}">${post.author}</a> on ${post.timestamp}</p>
                        <a href="#" id="like${post.id}" style="margin-right:2rem;">❤️ ${likes}</a>
                    <div>`;      
                    
                    container.appendChild(div);
                }
                
                b_like = document.querySelector(`#like${post.id}`);
                if(post.liked_by.includes(curUsername)){
                    b_like.className = "btn btn-danger";
                } else {
                    b_like.className = "btn btn-outline-danger";
                }

                b_like.addEventListener('click', function() {
                    postid = this.id.slice(4)
                    console.log(`post/${postid}`)
                    fetch(`/post/${postid}`, {
                        method: 'PUT',
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
                            this.className = "btn btn-danger";
                        } else if(action == "Unliked"){
                            this.textContent = `❤️ ${likeCount - 1}`
                            this.className = "btn btn-outline-danger";
                        }
                    })
                })
            }
        }
    })
}