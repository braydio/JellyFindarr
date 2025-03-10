
// mediaSearch.js - ES Module for JellyFindarr

const currentPage = { tv: 1, movie: 1 };

async function searchMedia(type, page) {
    let query = document.getElementById(type === 'tv' ? "tvShowInput" : "movieInput").value;
    if (!query.trim()) return alert("Please enter a name");

    let searchButton = document.getElementById(type === 'tv' ? "searchTv" : "searchMovie");
    setLoadingState(searchButton, true);

    try {
        let response = await fetch(`/search?query=${encodeURIComponent(query)}&type=${type}&page=${page}`);
        let results = await response.json();

        let resultList = document.getElementById(type === 'tv' ? "tvShowResults" : "movieResults");
        resultList.innerHTML = ""; // Clear previous results

        if (results.error || results.items.length === 0) {
            resultList.innerHTML = `<li>No results found</li>`;
            return;
        }

        results.items.forEach(item => {
            // Ensure the item has the type property for later use
            item.type = type;
            let listItem = document.createElement("li");
            listItem.innerHTML = `${item.title} (${item.year || "Unknown Year"}) 
                <button class="details-btn" data-item='${JSON.stringify(item)}'>Details</button> 
                <button class="request-btn" data-id="${item.id}" data-title="${item.title}" data-year="${item.year}" data-type="${type}">Request</button>`;
            resultList.appendChild(listItem);
        });

        // Show Back to Home button
        document.getElementById("backToHome").style.display = "block";

        // Handle pagination buttons
        currentPage[type] = page;
        document.getElementById(type === 'tv' ? "prevTvPage" : "prevMoviePage").disabled = page <= 1;
        document.getElementById(type === 'tv' ? "nextTvPage" : "nextMoviePage").disabled = !results.hasNextPage;

        // Attach event listeners dynamically
        attachEventListeners();

    } catch (error) {
        alert("Failed to search. Ensure the backend is running.");
    } finally {
        setLoadingState(searchButton, false);
    }
}

async function requestMedia(id, title, year, type, seasons = null) {
    if (!id) return alert("Invalid selection.");

    // Find the button that initiated the request (if any)
    let requestButton = document.querySelector(`button.request-btn[data-id="${id}"]`);
    if (requestButton) setLoadingState(requestButton, true);

    try {
        let payload = { id, title, year, type };
        if (seasons) payload.seasons = seasons;
        // Use a relative URL instead of "localhost"
        let response = await fetch("/request", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        let result = await response.json();
        alert(result.message || "Error: " + JSON.stringify(result.error));

    } catch (error) {
        alert("Failed to send request.");
    } finally {
        if (requestButton) setLoadingState(requestButton, false);
    }
}

function setLoadingState(button, isLoading) {
    if (!button) return;
    if (isLoading) {
        button.dataset.originalText = button.innerText;
        button.innerText = "Loading...";
        button.classList.add("loading");
        button.disabled = true;
    } else {
        button.innerText = button.dataset.originalText;
        button.classList.remove("loading");
        button.disabled = false;
    }
}

function changePage(type, direction) {
    searchMedia(type, currentPage[type] + direction);
}

function showDetails(item) {
    // Populate basic details
    document.getElementById("detailsTitle").innerText = item.title;
    document.getElementById("detailsPoster").src = item.poster || "https://via.placeholder.com/200";
    document.getElementById("detailsOverview").innerText = item.overview || "No overview available.";
    document.getElementById("detailsYear").innerText = item.year || "Unknown";
    document.getElementById("detailsGenres").innerText = item.genres ? item.genres.join(", ") : "N/A";
    document.getElementById("detailsRatings").innerText = item.ratings?.value ? `${item.ratings.value}/10` : "N/A";

    // Show or hide the "Seasons" detail placeholder (only for TV shows)
    const seasonsLabel = document.getElementById("detailsSeasons");
    if (item.type === "tv") {
        seasonsLabel.parentElement.style.display = "block";
    } else {
        seasonsLabel.parentElement.style.display = "none";
    }

    // Clear any existing extra details (seasons or box set info)
    let extraDetails = document.getElementById("extraDetails");
    if (!extraDetails) {
        extraDetails = document.createElement("div");
        extraDetails.id = "extraDetails";
        // Insert extraDetails before the modal's close button
        const modal = document.getElementById("detailsModal");
        modal.insertBefore(extraDetails, document.getElementById("closeModal"));
    }
    extraDetails.innerHTML = "";

    // Only for TV shows: add season selection if seasonCount exists
    if (item.type === "tv" && item.seasonCount) {
        let seasonCount = item.seasonCount;
        let seasonForm = document.createElement("form");
        seasonForm.id = "seasonForm";
        seasonForm.innerHTML = "<p>Select Seasons to Request:</p>";
        for (let i = 1; i <= seasonCount; i++) {
            let label = document.createElement("label");
            label.style.marginRight = "10px";
            let checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.value = i;
            checkbox.name = "season";
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(" Season " + i));
            seasonForm.appendChild(label);
        }
        extraDetails.appendChild(seasonForm);
    }
    // For Movies: if a boxSet array is provided and not empty, add a link to view the box set
    else if (item.type === "movie" && item.boxSet && item.boxSet.length > 0) {
        let boxSetLink = document.createElement("a");
        boxSetLink.href = "#";
        boxSetLink.innerText = "View Box Set Movies";
        boxSetLink.style.display = "block";
        boxSetLink.style.marginBottom = "10px";
        boxSetLink.addEventListener("click", (e) => {
            e.preventDefault();
            alert("Box Set: " + item.boxSet.join(", "));
        });
        extraDetails.appendChild(boxSetLink);
    }

    // Add a "Request" button to the modal if not already present
    let requestModalBtn = document.getElementById("modalRequestBtn");
    if (!requestModalBtn) {
        requestModalBtn = document.createElement("button");
        requestModalBtn.id = "modalRequestBtn";
        requestModalBtn.innerText = "Request";
        document.getElementById("detailsModal").appendChild(requestModalBtn);
    }
    // Remove any previous event listeners on the modal request button
    requestModalBtn.replaceWith(requestModalBtn.cloneNode(true));
    requestModalBtn = document.getElementById("modalRequestBtn");
    requestModalBtn.addEventListener("click", () => {
        if (item.type === "tv") {
            // For TV shows, collect selected seasons from the form
            const selectedSeasons = Array.from(document.querySelectorAll("#seasonForm input[name='season']:checked")).map(cb => cb.value);
            if (selectedSeasons.length === 0) {
                return alert("Please select at least one season.");
            }
            requestMedia(item.id, item.title, item.year, "tv", selectedSeasons);
        } else {
            // For movies, no extra info needed
            requestMedia(item.id, item.title, item.year, "movie");
        }
    });

    // Show the modal
    document.getElementById("detailsModal").style.display = "block";
}

function closeModal() {
    document.getElementById("detailsModal").style.display = "none";
}

function goBackToHome() {
    document.getElementById("tvShowResults").innerHTML = "";
    document.getElementById("movieResults").innerHTML = "";
    document.getElementById("backToHome").style.display = "none";
}

// Attach event listeners dynamically
function attachEventListeners() {
    document.querySelectorAll(".details-btn").forEach(button => {
        button.addEventListener("click", (event) => {
            const item = JSON.parse(event.target.dataset.item);
            showDetails(item);
        });
    });

    document.querySelectorAll(".request-btn").forEach(button => {
        button.addEventListener("click", (event) => {
            const id = event.target.dataset.id;
            const title = event.target.dataset.title;
            const year = event.target.dataset.year;
            const type = event.target.dataset.type;
            requestMedia(id, title, year, type);
        });
    });
}

// Export functions so they can be used in other modules if needed
export { searchMedia, changePage, showDetails, closeModal, requestMedia, goBackToHome };

