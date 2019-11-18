console.log("hello world");
initApp = function() {
    firebase.auth().onAuthStateChanged(function(user) {
        if(!user){
            window.location.href=("/login");
        }
    }, function(error){
        console.log(error);
    })
}
window.addEventListener('load', function() {
    initApp();
    });