// Daily navigation
const itineraryPage = document.querySelector("#itinerary-page");

const previousDayButton = document.querySelector("#previous-day");
const nextDayButton = document.querySelector("#next-day");
const nativeDate = document.querySelector("#nativeDate");

if (itineraryPage) {
    const currentDay = parseInt(
        itineraryPage.dataset.currentDay,
        10
    );

    const maxDay = parseInt(
        itineraryPage.dataset.maxDay,
        10
    );

    const itineraryUrl =
        itineraryPage.dataset.itineraryUrl;

    if (previousDayButton) {
        previousDayButton.addEventListener("click", () => {
            if (currentDay > 1) {
                window.location.href =
                    itineraryUrl + "?day=" + (currentDay - 1);
            }
        });
    }

    if (nextDayButton) {
        nextDayButton.addEventListener("click", () => {
            if (currentDay < maxDay) {
                window.location.href =
                    itineraryUrl + "?day=" + (currentDay + 1);
            }
        });
    }

    if (nativeDate) {
        nativeDate.addEventListener("change", () => {
            if (nativeDate.value) {
                window.location.href =
                    itineraryUrl + "?date=" + nativeDate.value;
            }
        });
    }
}

// Weekly navigation
const previousWeekButton = document.querySelector("#previous-week");
const nextWeekButton = document.querySelector("#next-week");
const weekCounter = document.querySelector("#week-counter");
const weekDate = document.querySelector("#week-dates");

let currentWeek = 1;
let maxWeek = 2;

function formatDate(date) {
    return date.toLocaleDateString("en-GB", {
        day: "numeric",
        month: "short",
        year: "numeric"
    });
}

function updateWeek() {
    if (!itineraryPage) {
        return;
    }

    const startDateString = itineraryPage.dataset.startDate;

    if (!startDateString) {
        return;
    }

    const startDate = new Date(startDateString + "T00:00:00");

    const weekStart = new Date(startDate);

    weekStart.setDate(
        startDate.getDate() + (currentWeek - 1) * 7
    );

    const weekEnd = new Date(weekStart);

    weekEnd.setDate(
        weekStart.getDate() + 6
    );

    if (weekCounter) {
        weekCounter.textContent = `Week ${currentWeek}`;
    }

    if (weekDate) {
        weekDate.textContent =
            `${formatDate(weekStart)} - ${formatDate(weekEnd)}`;
    }
}

if (previousWeekButton) {
    previousWeekButton.addEventListener("click", () => {
        if (currentWeek > 1) {
            currentWeek--;
            updateWeek();
        }
    });
}

if (nextWeekButton) {
    nextWeekButton.addEventListener("click", () => {
        if (currentWeek < maxWeek) {
            currentWeek++;
            updateWeek();
        }
    });
}

// Details modal update
const detailsActivityName = document.querySelector("#detailsModalTitle");
const detailsStartTime = document.querySelector("#detailsStartTime");
const detailsEndTime = document.querySelector("#detailsEndTime");
const detailsLocation = document.querySelector("#detailsLocation");
const detailsAddress = document.querySelector("#detailsAddress");
const detailsCreatedBy = document.querySelector("#detailsCreatedBy");
const detailsNotes = document.querySelector("#detailsNotes");

const noteLinks = document.querySelectorAll(".view-details");

noteLinks.forEach(link => {
    link.addEventListener("click", () => {

        const name = link.dataset.name;
        const startTime = link.dataset.startTime;
        const endTime = link.dataset.endTime;
        const location = link.dataset.location;
        const address = link.dataset.address;
        const createdBy = link.dataset.createdBy;
        const notes = link.dataset.notes;


        if (detailsActivityName) {
            detailsActivityName.textContent = name;
        }

        if (detailsStartTime) {
            detailsStartTime.textContent = startTime || "-";
        }

        if (detailsEndTime) {
            detailsEndTime.textContent = endTime || "-";
        }

        if (detailsLocation) {
            detailsLocation.textContent = location || "-";
        }

        if (detailsAddress) {
            detailsAddress.textContent = address || "-";
        }

        if (detailsCreatedBy) {
            detailsCreatedBy.textContent = createdBy || "-";
        }

        if (detailsNotes) {
            detailsNotes.textContent = notes || "No notes available.";
        }
    });
});

// Delete activity modal
const deleteButtons = document.querySelectorAll(".delete-activity-btn");
const deleteForm = document.getElementById("deleteActivityForm");
const deleteActivityName = document.getElementById("deleteActivityName");
const deleteActivityDay = document.getElementById("deleteActivityDay");

deleteButtons.forEach(button => {
    button.addEventListener("click", () => {

        const activityId = button.dataset.activityId;
        const currentDay = button.dataset.currentDay;
        const activityName = button.dataset.activityName;

        deleteForm.action = `/itinerary/delete/${activityId}`;

        deleteActivityDay.value = currentDay;
        deleteActivityName.textContent = activityName;
    });
});

// Edit activity modal
const editButtons = document.querySelectorAll(".edit-activity-btn");

const editForm = document.querySelector("#editActivityForm");
const editName = document.querySelector("#editActivityName");
const editStartTime = document.querySelector("#editActivityStartTime");
const editEndTime = document.querySelector("#editActivityEndTime");
const editLocation = document.querySelector("#editActivityLocation");
const editNotes = document.querySelector("#editActivityNotes");
const editDay = document.querySelector("#editActivityDay");

editButtons.forEach(button => {
    button.addEventListener("click", async () => {

        const activityId = button.dataset.activityId;
        const currentLocation = button.dataset.location;
        const currentAddress = button.dataset.address;

        editForm.action = `/itinerary/edit/${activityId}`;

        editName.value = button.dataset.activityName;
        editStartTime.value = button.dataset.startTime;
        editEndTime.value = button.dataset.endTime;
        editNotes.value = button.dataset.notes;
        editDay.value = button.dataset.currentDay;

        document.getElementById("editLocation").value = currentLocation;
        document.getElementById("editAddress").value = currentAddress;

        await initLocationSearch(
            "editActivityLocation",
            currentLocation,
            "editLocation",
            "editAddress",
            "editPlaceId"
        );
    });
});

// Add activity modal
const addDay = document.querySelector("#addActivityDay");

if (addDay && itineraryPage) {
    addDay.value = itineraryPage.dataset.currentDay;
}

// Location search
async function initLocationSearch(
    element_id,
    current_location,
    hiddenLocationId,
    hiddenAddressId,
    hiddenPlaceId
) {
    const { PlaceAutocompleteElement } =
        await google.maps.importLibrary("places");

    const container = document.getElementById(element_id);

    if (!container) return;

    container.innerHTML = "";

    const autocomplete = new PlaceAutocompleteElement();

    autocomplete.placeholder = "Search location name";

    if (current_location) {
        autocomplete.value = current_location;
    }

    container.appendChild(autocomplete);

    autocomplete.addEventListener(
        "gmp-select",
        async ({ placePrediction }) => {

            const place = placePrediction.toPlace();

            await place.fetchFields({
                fields: [
                    "displayName",
                    "formattedAddress",
                    "location",
                    "id"
                ]
            });

            // Location name
            document.getElementById(hiddenLocationId).value =
                place.displayName;

            // Address
            document.getElementById(hiddenAddressId).value =
                place.formattedAddress;

            // Google Place ID
            document.getElementById(hiddenPlaceId).value =
                place.id;
        }
    );
}

initLocationSearch(
    "addActivityLocation",
    "",
    "addLocation",
    "addAddress",
    "addPlaceId"
);

// Drag and drop activities
const timeline = document.querySelector("#itinerary-timeline");
const unassignedPanel = document.querySelector("#unassigned-activities");

const draggableActivities = document.querySelectorAll(
    ".activity-card, .unassigned-activity"
);

let draggedActivityId = null;
let draggedCard = null;
let dragOffsetY = 0;
let draggedDurationMinutes = 60;
let preview = null;


// Convert minutes to HH:MM
function minutesToTime(totalMinutes) {

    totalMinutes = Math.max(
        0,
        Math.min(totalMinutes, 1440)
    );

    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;

    return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}`;
}


// Get activity duration
function getDuration(card) {

    const start = card.dataset.startTime;
    const end = card.dataset.endTime;

    if (start && end) {

        const [startHour, startMinute] =
            start.split(":").map(Number);

        const [endHour, endMinute] =
            end.split(":").map(Number);

        let startMinutes =
            startHour * 60 + startMinute;

        let endMinutes =
            endHour * 60 + endMinute;

        if (endMinutes <= startMinutes) {
            endMinutes += 1440;
        }

        return endMinutes - startMinutes;
    }

    return 60;
}


// Drag start
draggableActivities.forEach(card => {

    card.addEventListener("dragstart", event => {

        draggedActivityId =
            card.dataset.activityId;

        draggedCard = card;

        // Get mouse position inside card
        const cardRect =
            card.getBoundingClientRect();

        dragOffsetY =
            event.clientY - cardRect.top;

        draggedDurationMinutes =
            getDuration(card);

        event.dataTransfer.setData(
            "activityId",
            draggedActivityId
        );

        event.dataTransfer.effectAllowed =
            "move";

        card.classList.add("dragging");


        // Create preview
        if (timeline) {

            preview =
                document.createElement("div");

            preview.className =
                "drop-preview";

            const timelineHeight =
                timeline.getBoundingClientRect().height;

            const heightPercent =
                (draggedDurationMinutes / 1440) * 100;

            preview.style.height =
                `${heightPercent}%`;

            timeline.appendChild(preview);
        }
    });


    card.addEventListener("dragend", () => {

        card.classList.remove("dragging");

        if (preview) {
            preview.remove();
            preview = null;
        }

        draggedActivityId = null;
        draggedCard = null;
    });
});


// Calculate drop position
function calculateDropMinutes(event) {

    if (!timeline) {
        return 0;
    }

    const rect =
        timeline.getBoundingClientRect();

    // Account for where the card was grabbed
    const y =
        event.clientY -
        rect.top -
        dragOffsetY;

    const minutesPerPixel =
        1440 / rect.height;

    let minutes =
        y * minutesPerPixel;

    // Snap to 15 minutes
    minutes =
        Math.round(minutes / 15) * 15;

    // Keep activity inside the day
    minutes =
        Math.max(
            0,
            Math.min(
                minutes,
                1440 - draggedDurationMinutes
            )
        );

    return minutes;
}


// Update preview
if (timeline) {

    timeline.addEventListener("dragover", event => {

        event.preventDefault();

        event.dataTransfer.dropEffect =
            "move";


        if (!preview) {
            return;
        }


        const minutes =
            calculateDropMinutes(event);

        const topPercent =
            (minutes / 1440) * 100;


        preview.style.top =
            `${topPercent}%`;
    });


    // Drop into timeline
    timeline.addEventListener("drop", async event => {

        event.preventDefault();

        const activityId =
            event.dataTransfer.getData("activityId");

        if (!activityId) {
            return;
        }


        const newStartMinutes =
            calculateDropMinutes(event);

        const newEndMinutes =
            newStartMinutes +
            draggedDurationMinutes;


        const startTime =
            minutesToTime(newStartMinutes);

        const endTime =
            minutesToTime(newEndMinutes);


        const selectedDate =
            document.querySelector(
                "#nativeDate"
            ).value;


        const formData =
            new FormData();

        formData.append(
            "date",
            selectedDate
        );

        formData.append(
            "start_time",
            startTime
        );

        formData.append(
            "end_time",
            endTime
        );


        const response =
            await fetch(
                `/itinerary/move/${activityId}`,
                {
                    method: "POST",
                    body: formData
                }
            );


        if (response.ok) {

            // Remember scroll position
            const timelineContainer =
                document.querySelector(
                    ".overflow-auto"
                );

            if (timelineContainer) {

                sessionStorage.setItem(
                    "timelineScroll",
                    timelineContainer.scrollTop
                );
            }

            window.location.reload();
        }
    });
}


// Drop into side panel
if (unassignedPanel) {

    unassignedPanel.addEventListener(
        "dragover",
        event => {

            event.preventDefault();

            event.dataTransfer.dropEffect =
                "move";
        }
    );


    unassignedPanel.addEventListener(
        "drop",
        async event => {

            event.preventDefault();

            const activityId =
                event.dataTransfer.getData(
                    "activityId"
                );

            if (!activityId) {
                return;
            }


            const formData =
                new FormData();

            formData.append(
                "date",
                ""
            );

            formData.append(
                "start_time",
                ""
            );

            formData.append(
                "end_time",
                ""
            );


            const response =
                await fetch(
                    `/itinerary/move/${activityId}`,
                    {
                        method: "POST",
                        body: formData
                    }
                );


            if (response.ok) {
                window.location.reload();
            }
        }
    );
}


// Restore scroll position so scroll doesn't snap to the top on reload
window.addEventListener("load", () => {

    const savedScroll =
        sessionStorage.getItem(
            "timelineScroll"
        );

    const timelineContainer =
        document.querySelector(
            ".overflow-auto"
        );

    if (
        savedScroll !== null &&
        timelineContainer
    ) {

        timelineContainer.scrollTop =
            parseInt(savedScroll, 10);

        sessionStorage.removeItem(
            "timelineScroll"
        );
    }
});