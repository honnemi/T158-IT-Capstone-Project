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
                    itineraryUrl +
                    "?day=" +
                    (currentDay - 1);

            }

        });

    }

    if (nextDayButton) {

        nextDayButton.addEventListener("click", () => {

            if (currentDay < maxDay) {

                window.location.href =
                    itineraryUrl +
                    "?day=" +
                    (currentDay + 1);

            }

        });

    }

    if (nativeDate) {

        nativeDate.addEventListener("change", () => {

            if (nativeDate.value) {

                window.location.href =
                    itineraryUrl +
                    "?date=" +
                    nativeDate.value;

            }

        });

    }

}

const previousWeekButton =
    document.querySelector("#previous-week");

const nextWeekButton =
    document.querySelector("#next-week");

const weekCounter =
    document.querySelector("#week-counter");

const weekDate =
    document.querySelector("#week-date");

let currentWeek = 1;
const maxWeek = 2;

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

    const startDateString =
        itineraryPage.dataset.startDate;

    if (!startDateString) {
        return;
    }

    const startDate =
        new Date(startDateString + "T00:00:00");

    const weekStart =
        new Date(startDate);

    weekStart.setDate(
        weekStart.getDate() +
        ((currentWeek - 1) * 7)
    );

    const weekEnd =
        new Date(weekStart);

    weekEnd.setDate(
        weekEnd.getDate() + 6
    );

    if (weekCounter) {

        weekCounter.textContent =
            `Week ${currentWeek}`;

    }

    if (weekDate) {

        weekDate.textContent =
            `${formatDate(weekStart)} - ${formatDate(weekEnd)}`;

    }

    if (previousWeekButton) {

        previousWeekButton.disabled =
            currentWeek <= 1;

    }

    if (nextWeekButton) {

        nextWeekButton.disabled =
            currentWeek >= maxWeek;

    }

}

if (previousWeekButton) {

    previousWeekButton.addEventListener(
        "click",
        () => {

            if (currentWeek > 1) {

                currentWeek--;

                updateWeek();

            }

        }
    );

}

if (nextWeekButton) {

    nextWeekButton.addEventListener(
        "click",
        () => {

            if (currentWeek < maxWeek) {

                currentWeek++;

                updateWeek();

            }

        }
    );

}

updateWeek();

const detailsActivityName =
    document.querySelector("#detailsModalTitle");

const detailsStartTime =
    document.querySelector("#detailsStartTime");

const detailsEndTime =
    document.querySelector("#detailsEndTime");

const detailsLocation =
    document.querySelector("#detailsLocation");

const detailsAddress =
    document.querySelector("#detailsAddress");

const detailsCreatedBy =
    document.querySelector("#detailsCreatedBy");

const detailsUpdatedBy =
    document.querySelector("#detailsUpdatedBy");

const detailsUpdatedAt =
    document.querySelector("#detailsUpdatedAt");

const detailsNotes =
    document.querySelector("#detailsNotes");

const noteLinks =
    document.querySelectorAll(".view-details");

noteLinks.forEach(link => {

    link.addEventListener("click", () => {

        const name =
            link.dataset.name;

        const startTime =
            link.dataset.startTime;

        const endTime =
            link.dataset.endTime;

        const location =
            link.dataset.location;

        const address =
            link.dataset.address;

        const createdBy =
            link.dataset.createdBy;

        const notes =
            link.dataset.notes;

        const updatedBy =
            link.dataset.updatedBy;

        const updatedAt =
            link.dataset.updatedAt;

        if (detailsActivityName) {

            detailsActivityName.textContent =
                name || "Details";

        }

        if (detailsStartTime) {

            detailsStartTime.textContent =
                startTime || "-";

        }

        if (detailsEndTime) {

            detailsEndTime.textContent =
                endTime || "-";

        }

        if (detailsLocation) {

            detailsLocation.textContent =
                location || "-";

        }

        if (detailsAddress) {

            detailsAddress.textContent =
                address || "-";

        }

        if (detailsCreatedBy) {

            detailsCreatedBy.textContent =
                createdBy || "-";

        }

        if (detailsUpdatedBy) {

            detailsUpdatedBy.textContent =
                updatedBy || "-";

        }

        if (detailsUpdatedAt) {

            detailsUpdatedAt.textContent =
                updatedAt || "-";

        }

        if (detailsNotes) {

            detailsNotes.textContent =
                notes || "No notes available.";

        }

    });

});


const deleteActivityButtons =
    document.querySelectorAll(".delete-activity-btn");

const deleteActivityForm =
    document.querySelector("#deleteActivityForm");

const deleteActivityName =
    document.querySelector("#deleteActivityName");

const deleteActivityDay =
    document.querySelector("#deleteActivityDay");

deleteActivityButtons.forEach(button => {

    button.addEventListener("click", () => {

        const activityId =
            button.dataset.activityId;

        const activityName =
            button.dataset.activityName;

        const day =
            button.dataset.currentDay;

        if (deleteActivityForm) {

            deleteActivityForm.action =
                `/itinerary/delete/${activityId}`;

        }

        if (deleteActivityName) {

            deleteActivityName.textContent =
                activityName || "this activity";

        }

        if (deleteActivityDay) {

            deleteActivityDay.value =
                day || "";

        }

    });

});


const editActivityButtons =
    document.querySelectorAll(".edit-activity-btn");

const editActivityForm =
    document.querySelector("#editActivityForm");

const editActivityName =
    document.querySelector("#editActivityName");

const editActivityStartTime =
    document.querySelector("#editActivityStartTime");

const editActivityEndTime =
    document.querySelector("#editActivityEndTime");

const editActivityNotes =
    document.querySelector("#editActivityNotes");

const editActivityDay =
    document.querySelector("#editActivityDay");

editActivityButtons.forEach(button => {

    button.addEventListener("click", () => {

        const activityId =
            button.dataset.activityId;

        const activityName =
            button.dataset.activityName;

        const startTime =
            button.dataset.startTime;

        const endTime =
            button.dataset.endTime;

        const currentLocation =
            button.dataset.location || "";

        const currentAddress =
            button.dataset.address || "";

        const notes =
            button.dataset.notes || "";

        const currentDay =
            button.dataset.currentDay;

        if (editActivityForm) {

            editActivityForm.action =
                `/itinerary/edit/${activityId}`;

        }

        if (editActivityName) {

            editActivityName.value =
                activityName || "";

        }

        if (editActivityStartTime) {

            editActivityStartTime.value =
                startTime || "";

        }

        if (editActivityEndTime) {

            editActivityEndTime.value =
                endTime || "";

        }

        if (editActivityNotes) {

            editActivityNotes.value =
                notes || "";

        }

        if (editActivityDay) {

            editActivityDay.value =
                currentDay || "";

        }

        const editLocation =
            document.querySelector("#editLocation");

        const editAddress =
            document.querySelector("#editAddress");

        if (editLocation) {

            editLocation.value =
                currentLocation;

        }

        if (editAddress) {

            editAddress.value =
                currentAddress;

        }

        // Initialise Google Places search
        if (
            typeof google !== "undefined" &&
            google.maps &&
            google.maps.importLibrary
        ) {

            initLocationSearch(
                "editActivityLocation",
                currentLocation,
                "editLocation",
                "editAddress",
                "editPlaceId"
            );

        }

    });

});

const addActivityModal =
    document.querySelector("#addActivityModal");

if (addActivityModal) {

    addActivityModal.addEventListener(
        "shown.bs.modal",
        () => {

            if (
                typeof google !== "undefined" &&
                google.maps &&
                google.maps.importLibrary
            ) {

                initLocationSearch(
                    "addActivityLocation",
                    "",
                    "addLocation",
                    "addAddress",
                    "addPlaceId"
                );

            }

        }
    );

}


async function initLocationSearch(
    element_id,
    current_location,
    hiddenLocationId,
    hiddenAddressId,
    hiddenPlaceId
) {

    try {

        const {
            PlaceAutocompleteElement
        } = await google.maps.importLibrary("places");

        const container =
            document.getElementById(element_id);

        if (!container) {
            return;
        }

        container.innerHTML = "";

        const autocomplete =
            new PlaceAutocompleteElement();

        autocomplete.placeholder =
            "Search location name";

        if (current_location) {

            autocomplete.value =
                current_location;

        }

        container.appendChild(
            autocomplete
        );

        autocomplete.addEventListener(
            "gmp-select",
            async ({ placePrediction }) => {

                try {

                    const place =
                        placePrediction.toPlace();

                    await place.fetchFields({
                        fields: [
                            "displayName",
                            "formattedAddress",
                            "location",
                            "id"
                        ]
                    });

                    const locationInput =
                        document.getElementById(
                            hiddenLocationId
                        );

                    const addressInput =
                        document.getElementById(
                            hiddenAddressId
                        );

                    const placeIdInput =
                        document.getElementById(
                            hiddenPlaceId
                        );

                    if (locationInput) {

                        locationInput.value =
                            place.displayName || "";

                    }

                    if (addressInput) {

                        addressInput.value =
                            place.formattedAddress || "";

                    }

                    if (placeIdInput) {

                        placeIdInput.value =
                            place.id || "";

                    }

                } catch (error) {

                    console.error(
                        "Error fetching place details:",
                        error
                    );

                }

            }
        );

    } catch (error) {

        console.error(
            "Error initialising Google Places:",
            error
        );

    }

}

const timeline =
    document.querySelector("#itinerary-timeline");

const unassignedActivities =
    document.querySelector("#unassigned-activities");

const draggableActivities =
    document.querySelectorAll(
        ".activity-card, .unassigned-activity"
    );

let draggedActivityId = null;
let draggedCard = null;
let dragOffsetY = 0;
let draggedDurationMinutes = 60;
let preview = null;

function timeToMinutes(time) {

    if (!time) {
        return 60;
    }

    const parts =
        time.split(":");

    const hours =
        parseInt(parts[0], 10);

    const minutes =
        parseInt(parts[1], 10);

    if (
        Number.isNaN(hours) ||
        Number.isNaN(minutes)
    ) {

        return 60;

    }

    return (
        hours * 60 +
        minutes
    );

}


function minutesToTime(totalMinutes) {

    totalMinutes =
        Math.max(
            0,
            Math.min(
                1439,
                totalMinutes
            )
        );

    const hours =
        Math.floor(
            totalMinutes / 60
        );

    const minutes =
        totalMinutes % 60;

    return (
        String(hours).padStart(2, "0") +
        ":" +
        String(minutes).padStart(2, "0")
    );

}


function getDuration(card) {

    const start =
        card.dataset.startTime;

    const end =
        card.dataset.endTime;

    if (!start || !end) {
        return 60;
    }

    const startMinutes =
        timeToMinutes(start);

    const endMinutes =
        timeToMinutes(end);

    let duration =
        endMinutes - startMinutes;

    if (duration <= 0) {
        duration = 60;
    }

    return duration;

}

draggableActivities.forEach(card => {

    card.addEventListener(
        "dragstart",
        event => {

            draggedActivityId =
                card.dataset.activityId;

            draggedCard =
                card;

            draggedDurationMinutes =
                getDuration(card);

            const rect =
                card.getBoundingClientRect();

            dragOffsetY =
                event.clientY -
                rect.top;

            card.classList.add(
                "opacity-50"
            );

            event.dataTransfer.effectAllowed =
                "move";

            event.dataTransfer.setData(
                "text/plain",
                draggedActivityId
            );

        }
    );


    card.addEventListener(
        "dragend",
        () => {

            card.classList.remove(
                "opacity-50"
            );

            if (preview) {

                preview.remove();

                preview = null;

            }

            draggedActivityId = null;
            draggedCard = null;

        }
    );

});

function calculateDropMinutes(event) {

    if (!timeline) {
        return 0;
    }

    const rect =
        timeline.getBoundingClientRect();

    const timelineHeight =
        timeline.scrollHeight;

    let y =
        event.clientY -
        rect.top +
        timeline.scrollTop -
        dragOffsetY;

    y =
        Math.max(
            0,
            Math.min(
                timelineHeight,
                y
            )
        );

    const minutesPerPixel =
        1440 / timelineHeight;

    let minutes =
        Math.round(
            y * minutesPerPixel
        );

    // Snap to 15-minute intervals
    minutes =
        Math.round(
            minutes / 15
        ) * 15;

    // Keep activity within the day
    minutes =
        Math.min(
            minutes,
            1440 - draggedDurationMinutes
        );

    return Math.max(
        0,
        minutes
    );

}

if (timeline) {

    timeline.addEventListener(
        "dragover",
        event => {

            event.preventDefault();

            event.dataTransfer.dropEffect =
                "move";

            if (!draggedCard) {
                return;
            }

            const dropMinutes =
                calculateDropMinutes(event);

            const timelineHeight =
                timeline.scrollHeight;

            const top =
                (
                    dropMinutes / 1440
                ) * timelineHeight;

            const height =
                (
                    draggedDurationMinutes /
                    1440
                ) * timelineHeight;

            if (!preview) {

                preview =
                    document.createElement(
                        "div"
                    );

                preview.className =
                    "position-absolute border border-primary rounded-3 bg-primary bg-opacity-10";

                preview.style.pointerEvents =
                    "none";

                preview.style.left =
                    "0";

                preview.style.right =
                    "0";

                preview.style.zIndex =
                    "5";

                timeline.appendChild(
                    preview
                );

            }

            preview.style.top =
                `${top}px`;

            preview.style.height =
                `${Math.max(height, 30)}px`;

        }
    );


    timeline.addEventListener(
        "drop",
        async event => {

            event.preventDefault();

            if (!draggedActivityId) {
                return;
            }

            const startMinutes =
                calculateDropMinutes(event);

            const endMinutes =
                Math.min(
                    1440,
                    startMinutes +
                    draggedDurationMinutes
                );

            const startTime =
                minutesToTime(
                    startMinutes
                );

            const endTime =
                minutesToTime(
                    endMinutes
                );

            const date =
                nativeDate
                    ? nativeDate.value
                    : "";

            try {

                const response =
                    await fetch(
                        `/itinerary/move/${draggedActivityId}`,
                        {
                            method: "POST",
                            headers: {
                                "Content-Type":
                                    "application/json"
                            },
                            body: JSON.stringify({
                                date: date,
                                start_time: startTime,
                                end_time: endTime
                            })
                        }
                    );

                if (!response.ok) {

                    throw new Error(
                        `HTTP ${response.status}`
                    );

                }

                sessionStorage.setItem(
                    "itineraryScrollTop",
                    document.querySelector(
                        ".overflow-auto"
                    )?.scrollTop || 0
                );

                window.location.reload();

            } catch (error) {

                console.error(
                    "Error moving activity:",
                    error
                );

            }

        }
    );

}

if (unassignedActivities) {

    unassignedActivities.addEventListener(
        "dragover",
        event => {

            event.preventDefault();

            event.dataTransfer.dropEffect =
                "move";

        }
    );


    unassignedActivities.addEventListener(
        "drop",
        async event => {

            event.preventDefault();

            if (!draggedActivityId) {
                return;
            }

            try {

                const response =
                    await fetch(
                        `/itinerary/move/${draggedActivityId}`,
                        {
                            method: "POST",
                            headers: {
                                "Content-Type":
                                    "application/json"
                            },
                            body: JSON.stringify({
                                date: null,
                                start_time: null,
                                end_time: null
                            })
                        }
                    );

                if (!response.ok) {

                    throw new Error(
                        `HTTP ${response.status}`
                    );

                }

                window.location.reload();

            } catch (error) {

                console.error(
                    "Error unassigning activity:",
                    error
                );

            }

        }
    );

}

window.addEventListener(
    "load",
    () => {

        const savedScroll =
            sessionStorage.getItem(
                "itineraryScrollTop"
            );

        if (!savedScroll) {
            return;
        }

        const scrollContainer =
            document.querySelector(
                ".overflow-auto"
            );

        if (scrollContainer) {

            scrollContainer.scrollTop =
                parseInt(
                    savedScroll,
                    10
                );

        }

        sessionStorage.removeItem(
            "itineraryScrollTop"
        );

    }
);