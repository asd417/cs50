

document.addEventListener('DOMContentLoaded', function() {
    console.log(`loggedinUser = ${document.querySelector('#Loggedinusername').innerHTML}`)
    if(document.querySelector('#Loggedinusername').innerHTML != "") {
        document.querySelector('#new_post').addEventListener('click',sendPost);
    }
    
    
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

function sendPost() {
    const csrftoken = getCookie('csrftoken')
    postContent = document.querySelector('#new_post_textarea').value

    fetch('/post', {
        credentials: 'include',
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            content: postContent,
        })
        //Need csrf in this POST request
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        loadPosts('all', 1);
    });
    
}