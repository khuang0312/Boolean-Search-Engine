function showQuery(query) {
    /* Uses template strings to display the query that the user chose...
    */
    document.getElementById("inputted_query").textContent = `Results for \'${query}\':`
}

function updateSearchResults(searchResults) {
    /* searchResults - an array of Strings or URLs
        takes a list of search results and creates a results list to display
    */
    let resultsList = "";     
    searchResults.forEach(element => {
        resultsList += "<li>" + element + "</li>"
    });
    document.getElementById("results_list").innerHTML = "<ol>" + resultsList + "</ol>";
}

function toggleResultsDisplay() {
    /* Hides or shows the "results" div
    */
    document.getElementById("results").toggleAttribute("hidden");
}

// function for parsing responses...