// $(document).ready(function() {
//     $(".sidebar ul li").on('click', function () {
//         $(".sidebar ul li.active").removeClass('active');
//         $(this).addClass('active');
//     });

//     $('.open-btn').on('click', function () {
//         if ($('.sidebar').hasClass('active')) {
//             $('.sidebar').removeClass('active');
//             $('.Main_window').removeClass('active');
//         } else {
//             $('.sidebar').addClass('active');
//             $('.Main_window').addClass('active');
//         }
//     });
// });

document.addEventListener("DOMContentLoaded", function () {
    const sidebarItems = document.querySelectorAll(".sidebar ul li");
    const sidebar = document.querySelector(".sidebar");
    const mainWindow = document.querySelector(".Main_window");

    sidebar.classList.remove("active");
    mainWindow.classList.remove("active");

    sidebarItems.forEach(item => {
        item.addEventListener("click", function () {
            sidebarItems.forEach(element => element.classList.remove("active"));
            this.classList.add("active");
        });
    });

    const openBtn = document.querySelector(".open-btn");

    openBtn.addEventListener("click", function () {

        if (sidebar.classList.contains("active")) {
            sidebar.classList.remove("active");
            mainWindow.classList.remove("active");
        } else {
            sidebar.classList.add("active");
            mainWindow.classList.add("active");
        }
    });

    // const logoutbtn = document.getElementById("logoutbtn");
    // const token = JSON.parse(localStorage.getItem("token"));
    // const decodedToken = jwt_decode(token);

    document.getElementById("loginBtn").addEventListener("click", function () {
        localStorage.removeItem("token");
        window.location.href = "../index.html";
    });

});
