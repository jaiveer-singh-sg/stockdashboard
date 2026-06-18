async function runSwingAI(){

// document.getElementById("ticker-input").value;

let ticker = document.getElementById("ticker-input").value.trim().toUpperCase();

let response =
await fetch(
"http://127.0.0.1:8000/swing-analysis",
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

ticker:ticker

})

});


let result =
await response.json();


document.getElementById(
"aiResult"
).textContent =
JSON.stringify(
result,
null,
2
);


}