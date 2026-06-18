async function runAIAnalysis(){

// document.getElementById("ticker-input").value;

let ticker = document.getElementById("ticker-input").value.trim().toUpperCase();

let response =
await fetch(
"http://localhost:8000/analyze",
{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({

ticker:ticker,

timeframe:"5-15 days"

})

});


let data =
await response.json();



document.getElementById(
"aiResult"
).textContent =
JSON.stringify(
data,
null,
2
);


}

