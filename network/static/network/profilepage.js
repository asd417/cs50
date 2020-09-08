document.addEventListener('DOMContentLoaded', function() {
    const pageusername = document.querySelector('#docname').innerHTML;
    b_follow = document.querySelector('#follow_button');
    fetch(`/follow/${pageusername}`,{
        credentials: 'include',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(response => {
        action = response.following;
        if(action) {
            b_follow.innerHTML = 'UnFollow'
        } else {
            b_follow.innerHTML = 'Follow'
        }
    })
    
    b_follow.addEventListener('click',follow);  
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

const csrftoken = getCookie('csrftoken')

function follow(){
    const pageusername = document.querySelector('#docname').innerHTML;
    
    fetch(`/follow/${pageusername}`,{
        credentials: 'include',
        method: 'PUT',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            follow: true,
        })
    })
    .then(response => response.json())
    .then(response => {
        action = response.message.slice(13);
        console.log(action);
        if(action === "Followed") {
            followercounter = document.querySelector('#followerCount');
            count = parseInt(followercounter.innerHTML.slice(11)) + 1;
            followercounter.innerHTML = `Followers: ${count}`;
            b_follow = document.querySelector('#follow_button');
            b_follow.innerHTML = 'Unfollow';
        } else {
            followercounter = document.querySelector('#followerCount');
            count = parseInt(followercounter.innerHTML.slice(11)) - 1;
            followercounter.innerHTML = `Followers: ${count}`;
            b_follow = document.querySelector('#follow_button');
            b_follow.innerHTML = 'Follow';
        }
    })
    
}
