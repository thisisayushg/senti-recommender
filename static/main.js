document.addEventListener("DOMContentLoaded", () => {
    
    var xhr = new XMLHttpRequest();
    var availableUsers = [];
    xhr.responseType = "json";
    
    xhr.onload = () => {
        document.getElementsByClassName("loader")[0]
                .setAttribute("hidden", true);
        const response = xhr.response
        if(response === null){
            alert('Unable to fetch users')
        }
        if(response['users'].length > 0){
            availableUsers = response['users']
        }
        const autoCompleteJS = new Autocomplete("#autocomplete", {
            autoSelect: true,
            debounceTime: 700,
            search: (input) => {
                if (input.length < 1) {
                    return [];
                }
                return availableUsers.filter((country) => {
                    return country.toLowerCase().includes(input.toLowerCase());
                });
            },
        });
    }
    document.getElementsByClassName("loader")[0].removeAttribute("hidden");
    xhr.open('GET', 'http://127.0.0.1:5000/users')
    xhr.send()


    document.getElementById("name").addEventListener("input", function () {
        if (!this.value)
            document
                .querySelector(".autocomplete  button")
                .setAttribute("disabled", true);
        else
            document
                .querySelector(".autocomplete  button")
                .removeAttribute("disabled");
    });
});

function getrecommendation() {
    document.getElementsByClassName("loader")[0].removeAttribute("hidden");
    let input = document.getElementById("name");
    var xhr = new XMLHttpRequest();
    xhr.responseType = "json";
    xhr.onload = () => {
        const response = xhr.response;
        if(response === null){
            // process died on heroku
            alert('Heroku: Process died due to R14 Memory Quota Exceeded (Default Quota 512MB for free tier)')
        }

        const table = document.getElementById("products");
        if(table.hasAttribute('hidden'))
            table.attributes.removeNamedItem("hidden");
        if(table.querySelector("tbody").childElementCount > 0){
            table.querySelector("tbody").innerHTML = ''
        }
        if (response["recommended_items"].length > 0)
            for (let item of response["recommended_items"]) {
                let row = document.createElement("tr");
                row.innerHTML = `
                <td class="text-primary">${item.name}</td>
                <td>${item.brand}</td>
                <td>${item.broad_category}</td>
                <td>${item.categories}</td>
            `;
                table.querySelector("tbody").appendChild(row);
            }
        else {
            let row = document.createElement("tr");
            row.innerHTML = `
            <td colspan="4" class="text-center">
                No Recommendations available for this user
            </td>
            `;
            table.querySelector("tbody").appendChild(row);
        }
        document
            .getElementsByClassName("loader")[0]
            .setAttribute("hidden", true);
    };
    xhr.open("GET", `http://127.0.0.1:5000/predict/${input.value}`);
    xhr.send();
}