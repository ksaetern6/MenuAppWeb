firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
       console.log("user is signed in");
    }
   else {
       console.log("user is not signed in");
     }
   })

var db = firebase.firestore();
var storage = firebase.storage();

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
                        var imgObj = new Image(300,300);
                        imgObj.src=url;
                        document.body.append(imgObj);
                    });
                });
            });

        } // if
    })
})