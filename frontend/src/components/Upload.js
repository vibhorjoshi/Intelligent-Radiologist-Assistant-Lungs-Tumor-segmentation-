import React, { useState } from 'react';

function Upload() {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async() => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/predict', {
            method: 'POST',
            body: formData,
        });
        const result = await response.json();
        console.log(result);
    };

    return ( <
        div >
        <
        input type = "file"
        onChange = { handleFileChange }
        /> <
        button onClick = { handleUpload } > Upload < /button> <
        /div>
    );
}

export default Upload;