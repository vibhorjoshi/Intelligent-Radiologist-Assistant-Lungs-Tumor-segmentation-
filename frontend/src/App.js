import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import { useState } from 'react';

// Login Component
function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = (e) => {
        e.preventDefault();
        if (username === 'doctor') {
            onLogin();
        }
    };

    return ( <
        form onSubmit = { handleLogin } >
        <
        input type = "text"
        placeholder = "Username"
        onChange = {
            (e) => setUsername(e.target.value) }
        /> <
        input type = "password"
        placeholder = "Password"
        onChange = {
            (e) => setPassword(e.target.value) }
        /> <
        button type = "submit" > Login < /button> <
        /form>
    );
}

// Dashboard Component
function Dashboard() {
    return <h1 > Welcome to the Dashboard < /h1>;
}

// App Component
function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    return ( <
        Router >
        <
        Switch >
        <
        Route exact path = "/" > {
            isLoggedIn ? < Redirect to = "/dashboard" / > : < Login onLogin = {
                () => setIsLoggedIn(true) }
            />} <
            /Route> <
            Route path = "/dashboard" > { isLoggedIn ? < Dashboard / > : < Redirect to = "/" / > } <
            /Route> <
            /Switch> <
            /Router>
        );
    }

    export default App;