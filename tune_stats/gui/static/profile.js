const viewOneMonthBtn = document.querySelector(".view-one-month-btn");
const viewSixMonthsBtn = document.querySelector(".view-six-months-btn");
const viewLifetimeBtn = document.querySelector(".view-lifetime-btn");

const oneMonth = document.getElementsByClassName("one-month")
const sixMonths = document.getElementsByClassName("six-months")
const lifetime = document.getElementsByClassName("lifetime")

const lightDarkColor = "%252525"
const orangeColor = "#E46249"

viewOneMonthBtn.addEventListener('click', event => {
    //display classes that have one month and hide those who don't
    for (const element of oneMonth) {
        element.classList.remove("hidden");
    }
    for (const element of sixMonths) {
        element.classList.add("hidden");
    }
    for (const element of lifetime) {
        element.classList.add("hidden");
    }

    viewOneMonthBtn.classList.add("button-toggled");
    viewOneMonthBtn.classList.remove("button-not-toggled");
    viewSixMonthsBtn.classList.remove("button-toggled");
    viewSixMonthsBtn.classList.add("button-not-toggled");
    viewLifetimeBtn.classList.remove("button-toggled");
    viewLifetimeBtn.classList.add("button-not-toggled");
});

viewSixMonthsBtn.addEventListener('click', event => {
    //display element that have class six months and hide those who don't
    for (const element of oneMonth) {
        element.classList.add("hidden");
    }
    for (const element of sixMonths) {
        element.classList.remove("hidden");
    }
    for (const element of lifetime) {
        element.classList.add("hidden");
    };
    
    viewOneMonthBtn.classList.remove("button-toggled");
    viewOneMonthBtn.classList.add("button-not-toggled");
    viewSixMonthsBtn.classList.add("button-toggled");
    viewSixMonthsBtn.classList.remove("button-not-toggled");
    viewLifetimeBtn.classList.remove("button-toggled");
    viewLifetimeBtn.classList.add("button-not-toggled");
});

viewLifetimeBtn.addEventListener('click', event => {
    //display elements that have class lifetime and hide those who don't
    for (const element of oneMonth) {
        element.classList.add("hidden");
    }
    for (const element of sixMonths) {
        element.classList.add("hidden");
    }
    for (const element of lifetime) {
        element.classList.remove("hidden");
    };
    viewOneMonthBtn.classList.remove("button-toggled");
    viewOneMonthBtn.classList.add("button-not-toggled");
    viewSixMonthsBtn.classList.remove("button-toggled");
    viewSixMonthsBtn.classList.add("button-not-toggled");
    viewLifetimeBtn.classList.add("button-toggled");
    viewLifetimeBtn.classList.remove("button-not-toggled");
});


const topTracksOneMonthBtn = document.querySelector(".top-tracks-one-month-btn");
const topTracksOneMonthMoreItems = document.querySelector(".top-tracks-one-month .more-items")
topTracksOneMonthBtn.addEventListener('click', event => {
    topTracksOneMonthMoreItems.classList.toggle("hidden")
})

const topArtistsOneMonthBtn = document.querySelector(".top-artists-one-month-btn");
const topArtistsOneMonthMoreItems = document.querySelector(".top-artists-one-month .more-items")
topArtistsOneMonthBtn.addEventListener('click', event => {
    topArtistsOneMonthMoreItems.classList.toggle("hidden")
});

const topTracksSixMonthsBtn = document.querySelector(".top-tracks-six-months-btn");
const topTracksSixMonthsMoreItems = document.querySelector(".top-tracks-six-months .more-items")
topTracksSixMonthsBtn.addEventListener('click', event => {
    topTracksSixMonthsMoreItems.classList.toggle("hidden")
});

const topArtistsSixMonthsBtn = document.querySelector(".top-artists-six-months-btn");
const topArtistsSixMonthsMoreItems = document.querySelector(".top-artists-six-months .more-items")
topArtistsSixMonthsBtn.addEventListener('click', event => {
    topArtistsSixMonthsMoreItems.classList.toggle("hidden")
});

const topTracksLifetimeBtn = document.querySelector(".top-tracks-lifetime-btn");
const topTracksLifetimeMoreItems = document.querySelector(".top-tracks-lifetime .more-items")
topTracksLifetimeBtn.addEventListener('click', event => {
    topTracksLifetimeMoreItems.classList.toggle("hidden")
});

const topArtistsLifetimeBtn = document.querySelector(".top-artists-lifetime-btn");
const topArtistsLifetimeMoreItems = document.querySelector(".top-artists-lifetime .more-items")
topArtistsLifetimeBtn.addEventListener('click', event => {
    topArtistsLifetimeMoreItems.classList.toggle("hidden")
});