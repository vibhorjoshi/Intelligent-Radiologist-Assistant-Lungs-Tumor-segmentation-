import React, { useState } from 'react';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        if (username === 'doctor') {
            console.log('Login successful');
            // Redirect logic would go here
        }
    };

    return ( <
        <
        form onSubmit = { handleLogin } >

        <
        /form> <
        input type = "text"
        placeholder = "Username"
        onChange = {
            (e) => setUsername(e.target.value)
        }
        /> <
        input type = "password"
        placeholder = "Password"
        onChange = {
            (e) => setPassword(e.target.value)
        }
        /> <
        button type = "submit" > Login < /button> < /
        form >
    );
}

export default Login;