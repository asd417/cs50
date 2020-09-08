document.addEventListener('DOMContentLoaded', function() {
    const pagename = document.querySelector('#docname').innerHTML;
    console.log(`pagename = ${pagename}`);
    if (pagename == '') {
        updatePagiNav('all');

        loadPosts('all', 1);
    } else {
        updatePagiNav(pagename);
        loadPosts(pagename, 1);
    }
    
})