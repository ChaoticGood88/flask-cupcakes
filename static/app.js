// Base URL for the API
const BASE_URL = "/api/cupcakes";

// Function to generate HTML for a single cupcake
function generateCupcakeHTML(cupcake) {
    return `
        <li data-cupcake-id="${cupcake.id}">
            <img src="${cupcake.image}" alt="(image of ${cupcake.flavor} cupcake)" width="100">
            ${cupcake.flavor} / ${cupcake.size} / Rating: ${cupcake.rating}
        </li>
    `;
}

// Fetch cupcakes from the API and display them on the page
async function showCupcakes() {
    try {
        const response = await axios.get(BASE_URL);
        const cupcakes = response.data.cupcakes;

        for (let cupcake of cupcakes) {
            $("#cupcake-list").append(generateCupcakeHTML(cupcake));
        }
    } catch (err) {
        console.error("Error fetching cupcakes:", err);
    }
}

// Handle form submission to add a new cupcake
$("#add-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();

    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = parseFloat($("#rating").val()); // Ensure rating is a float
    const image = $("#image").val() || "https://tinyurl.com/demo-cupcake";

    try {
        // Send POST request to API to add the new cupcake
        const response = await axios.post(BASE_URL, {
            flavor,
            size,
            rating,
            image
        });

        // Get the newly added cupcake data and append it to the list
        const newCupcake = response.data.cupcake;
        $("#cupcake-list").append(generateCupcakeHTML(newCupcake));

        // Clear the form inputs
        $("#add-cupcake-form").trigger("reset");
    } catch (err) {
        console.error("Error adding cupcake:", err);
    }
});

// Initial load of cupcakes
$(showCupcakes);
