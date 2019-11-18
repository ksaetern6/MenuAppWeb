var firebaseConfig = {
    apiKey: 'AIzaSyBMNp1j4Di3OaHlGPXJ9LuRvXMPAeMmcro',
    authDomain: "menuapp-f3764.firebaseapp.com",
    databaseURL: "https://menuapp-f3764.firebaseio.com",
    projectId: "menuapp-f3764",
    storageBucket: "menuapp-f3764.appspot.com",
    messagingSenderId: "77920760117",
    appId: "1:77920760117:web:67cf1a4799eb73e064dc7c",
    measurementId: "G-33NWQZKM7W"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
var db = firebase.firestore();
var storage = firebase.storage();
console.log("firebase initialized");

const pHeader = document.querySelector("#first-p");
const loadBtn = document.querySelector("#load");
const docRef = db.doc("Restaurants/E2zVURqnFMjg9t6bkfYs");

loadBtn.addEventListener("click",function() {
    docRef.get().then(function(doc) {
        if(doc && doc.exists) {
            const myData = doc.data();

            db.collection("/Restaurants/E2zVURqnFMjg9t6bkfYs/items").get()
            .then((querySnapshot) => {
                querySnapshot.forEach((doc) => {
                    console.log(`${doc.id} => ${doc.data().locationRef}`);
                    //imgList.push(doc.locationRef);
                    storage.refFromURL(doc.data().locationRef).getDownloadURL().then(function(url) {
                        var imgObj = new Image(500,300);
                        imgObj.src=url;
                        document.body.append(imgObj);
                    });
                });
            });

        } // if
    })
})