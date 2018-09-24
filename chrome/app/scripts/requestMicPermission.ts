const nav = <any>navigator;
nav.webkitGetUserMedia({ audio: true }, (stream: any) => {
    console.log(stream);
    const para = document.createElement("p");
    const node = document.createTextNode("Permission granted. You can close this tab");
    para.appendChild(node);

    const element = document.getElementById("content") as HTMLElement;
    element.appendChild(para);
},
    (err: any) => {
        /* handle the error */
        const para = document.createElement("p");
        const node = document.createTextNode("Permission not granted. Err: " + err.message);
        para.appendChild(node);

        const element = document.getElementById("content") as HTMLElement;
        element.appendChild(para);
    });
