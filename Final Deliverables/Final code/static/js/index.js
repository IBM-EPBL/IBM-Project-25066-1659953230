function jobs(n){
let text = document.querySelectorAll('card-title');
let text1 = text[n].innerHTML;
window.location.replace(window.location.href+'/apply', {
    job : text1
});
}

// function jobs(n){
//     let text = document.querySelectorAll('card-title');
//     let text1 = text[n].innerHTML;
//     $.ajax({
//         type: "POST",
//         url: "/login",
//         data: JSON.stringify(text1),
//         contentType: "application/json",
//         dataType: 'json',
//       });
// } 