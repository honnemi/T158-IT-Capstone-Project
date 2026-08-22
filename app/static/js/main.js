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
const nativeDate = document.querySelector("#nativeDate");
 
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


// Make sure date cannot be picked from calendar outside of the trip duration
function setDateLimits() {
    const tripEndDate = new Date(startDate);

    tripEndDate.setDate(
        startDate.getDate() + (maxDay - 1)
    );

    if (nativeDate) {
        nativeDate.min = formatDateForInput(startDate);
        nativeDate.max = formatDateForInput(tripEndDate);
    }
}

function formatDateForInput(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
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
    if (weekCounter) {
        weekCounter.textContent = `Week ${currentWeek}`; 
    }

    if (weekDate) {
        weekDate.textContent = 
            `${formatDate(weekStart)} - ${formatDate(weekEnd)}`;
    }
} 
 
function updateDay() { 
 
    const currentDate = new Date(startDate); 
 
    currentDate.setDate( 
        startDate.getDate() + (currentDay - 1) 
    ); 
 
    // Update text elements 
    if (dayCounter) {
        dayCounter.textContent = `Day ${currentDay}`; 
    }

    if (dayDate) {
        dayDate.textContent = formatDate(currentDate); 
    }

    if (nativeDate) {
        nativeDate.value = formatDateForInput(currentDate);
    }

    updateWeek();
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


// Handle calendar date changes
if (nativeDate) {
    nativeDate.addEventListener("change", () => {

        const selectedDate = new Date(nativeDate.value + "T00:00:00");

        const difference =
            selectedDate.getTime() - startDate.getTime();

        const differenceInDays =
            Math.round(difference / (1000 * 60 * 60 * 24));

        const selectedDay = differenceInDays + 1;

        if (selectedDay >= 1 && selectedDay <= maxDay) {
            currentDay = selectedDay;
            updateDay();
        }
    });
}


// Set initial date and enforce limits
setDateLimits();
updateDay();