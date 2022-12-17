/*
Author: Bill Tong
Objective: Adds dynamic functionality to Login form
*/

// Different forms in the login screen are available
const formContainer = document.querySelector('.container');
const loginForm = document.querySelector('#login-form');
const signupForm = document.querySelector('#signup-form');

// Transitions between login page & signup page
const switchTemplate = (form) => {
    if(form == 'create'){
        if(window.innerWidth > 800){
            formContainer.style.left = `50%`;
        }
        loginForm.style.marginLeft = `-150%`;
        signupForm.style.marginLeft = `-100%`;
    } else{
        if(window.innerWidth > 800){
            formContainer.style.left = `0%`;
        }
        loginForm.style.marginLeft = `0%`;
        signupForm.style.marginLeft = `50%`;
    }
}