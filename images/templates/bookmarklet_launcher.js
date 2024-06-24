(function () {
    if(!window.bookmarklet){
        bookmarklet_js = document.body.appendChild(document.createElement('script'));
        // Using a random number, we prevent the browser from loading
        // the file from the browser’s cache.
        bookmarklet_js.src = "127.0.0.1:8080/static/js/bookmarklet.js?r="+Math.floor(Math.random()*9999999999999999);
        window.bookmarklet = true;
    }
    else{
        bookmarkletLaunch();
    }
})();