// function ShowHideDiv() {
//         var ddlPassport = document.getElementById("ddlPassport");
//         var dvPassport = document.getElementById("dvPassport");
//         dvPassport.style.display = ddlPassport.value == "Y" ? "block" : "none";
//     }

function ShowHideDiv() {
    console.log("Function Called")
    let show = document.getElementById("account").value
    console.log(show)
    if (show == "student") {
        document.getElementById('student').style.display = "block"
        document.getElementById('teacher').style.display = "none"
    }

    else if (show == "teacher") {
        document.getElementById('student').style.display = "none"
        document.getElementById('teacher').style.display = "block"
    }
}