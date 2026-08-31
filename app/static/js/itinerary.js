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

// Notes modal update
const notesActivityName = document.querySelector("#notesActivityName");
const notesContent = document.querySelector("#notesContent");

const noteLinks = document.querySelectorAll(".view-notes");

noteLinks.forEach(link => {
    link.addEventListener("click", () => {

        const name = link.dataset.name;
        const notes = link.dataset.notes;

        if (notesActivityName) {
            notesActivityName.textContent = name;
        }

        if (notesContent) {
            notesContent.textContent = notes;
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
    button.addEventListener("click", () => {

        const activityId = button.dataset.activityId;

        editForm.action = `/itinerary/edit/${activityId}`;

        editName.value = button.dataset.activityName;
        editStartTime.value = button.dataset.startTime;
        editEndTime.value = button.dataset.endTime;
        editLocation.value = button.dataset.location;
        editNotes.value = button.dataset.notes;
        editDay.value = button.dataset.currentDay;
    });
});

// Add activity modal
const addDay = document.querySelector("#addActivityDay");

if (addDay && itineraryPage) {
    addDay.value = itineraryPage.dataset.currentDay;
}