console.log(document.getElementById("query_results_list"));
console.log("Hi");
console.log({{ results_string }});
document.getElementById("query_results_list").textContent = {{ results_string }};