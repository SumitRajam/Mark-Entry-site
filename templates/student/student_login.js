document.addEventListener("DOMContentLoaded", function () {
    var password = document.getElementById('loginPassword');
    var submit = document.getElementById('login');
    var email = document.getElementById('loginEmail');
    var evalid = document.getElementById('evalid');
    var passvalid = document.getElementById('passvalid');
    let errorflag = 0;

    function checkemail() {
        evalid.innerHTML = '';
        if (email.value.trim() === '') {
            evalid.innerHTML = "Email cannot be empty";
            errorflag = 1;
            email.style.borderColor = 'red';
        } else {
            let regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!regex.test(email.value.trim())) {
                evalid.innerHTML = "Please enter a valid email";
                email.style.borderColor = 'red';
                errorflag = 1;
            } else {
                email.style.borderColor = 'green';
            }
        }
    }

    function checkpass() {
        passvalid.innerHTML = '';
        if (password.value.trim() === '') {
            passvalid.innerHTML = "Password cannot be empty";
            errorflag = 1;
            password.style.borderColor = 'red';
        } else if (password.value.length < 8) {
            passvalid.innerHTML = "Password must contain at least 8 characters";
            errorflag = 1;
            password.style.borderColor = 'red';
        } else {
            password.style.borderColor = 'green';
        }
    }

    async function check() {
        errorflag = 0;
        checkemail();
        checkpass();
        if (errorflag === 0) {
            evalid.innerHTML = '';
            passvalid.innerHTML = '';

            const response = await fetch("http://127.0.0.1:5000/user/student/login", {
                method: "POST",
                body: JSON.stringify({
                    "email": email.value.trim(),
                    "password": password.value.trim()
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            });

            const data = await response.json();
            if (data.status === "success") {
                console.log("Login successful:", data);
                toastr.success('Student registered successfully');
                localStorage.removeItem("token");
                localStorage.setItem("token", JSON.stringify(data.data.token));

                window.location.href = "./student/student_home.html";
            } else {
                toastr.error('Oops! Something went wrong.');
            }
        }
    }

    submit.addEventListener('click', function (event) {
        event.preventDefault();
        check();
    });

    email.addEventListener('blur', checkemail);
    password.addEventListener('blur', checkpass);
    email.addEventListener('keyup', checkemail);
    password.addEventListener('keyup', checkpass);
});
