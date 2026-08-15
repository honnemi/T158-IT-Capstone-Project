const previousWeekButton = document.querySelector("#previous-week");
const nextWeekButton = document.querySelector("#next-week");
const weekCounter = document.querySelector("#week-counter");
const weekDate = document.querySelector("#week-dates");

let currentWeek = 1;
let maxWeek = 2;

const previousDayButton = document.querySelector("#previous-day");
const nextDayButton = document.querySelector("#next-day");
const dayCounter = document.querySelector("#day-counter");
const dayDate = document.querySelector("#date");

let currentDay = 1;
let maxDay = 14;

// Hard-coded state date (for now)
const startDate = new Date(2026, 6, 6);

function formatDate(date) {
    return date.toLocaleDateString("en-GB", {
        day: "numeric",
        month: "short",
        year: "numeric"
    });
}

function updateWeek() {

    const weekStart = new Date(startDate);

    // Sets week start so every week is calculated from this day on
    weekStart.setDate(
        startDate.getDate() + (currentWeek - 1) * 7
    );

    const weekEnd = new Date(weekStart);

    // Sets week end (6 days from week start)
    weekEnd.setDate(
        weekStart.getDate() + 6
    );

    // Update text elements
    weekCounter.textContent = `Week ${currentWeek}`;
    weekDate.textContent =
        `${formatDate(weekStart)} - ${formatDate(weekEnd)}`;
}

function updateDay() {

    const currentDate = new Date(startDate);

    currentDate.setDate(
        startDate.getDate() + (currentDay - 1)
    );

    // Update text elements
    dayCounter.textContent = `Day ${currentDay}`;
    dayDate.textContent = formatDate(currentDate);
}

// Handle button clicks
if (previousWeekButton && nextWeekButton) {
    previousWeekButton.addEventListener("click", () => {
        // Make sure week can't go below 1
        if (currentWeek > 1) {
            currentWeek--;
            updateWeek();
        }
    });

    nextWeekButton.addEventListener("click", () => {
        // Make sure week can't exceed hardcoded limit (end of trip)
        if (currentWeek != maxWeek) {
            currentWeek++;
            updateWeek();
        }
    });
    
}

if (previousDayButton && nextDayButton) {

    previousDayButton.addEventListener("click", () => {
        // Make sure day can't go below 1
        if (currentDay > 1) {
            currentDay--;
            updateDay();
        }
    });
    
    nextDayButton.addEventListener("click", () => {
        // Make sure day can't exceed hardcoded limit (end of trip)
        if (currentDay != maxDay) {
            currentDay++;
            updateDay();
        }
    });
}