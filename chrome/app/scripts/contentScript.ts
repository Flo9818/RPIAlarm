navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function (stream) {
        console.log(stream)
    })
    .catch(function (err) {
        /* handle the error */
        console.log(err);
    });
