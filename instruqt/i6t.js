// JavaScript for the Track 3 "course"

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    let expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');

    for (let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }

    return "";
}

const tracks = [
    { "slug": "track-t1", "token": "em_U2BYod2b-kJ_I0L7" },
    { "slug": "track-t2", "token": "em_nS-1JIuu7-myRcaS" },
    { "slug": "track-t3", "token": "em_ETLuLd7gy2rjFXhg", "button": "Get Certified!" },
    { "done": true },
]

function setPosition(position) {
    const i6tPosition = position.toString();
    setCookie("i6t-position", i6tPosition, 365);
}

function getPosition() {
    cookieString = getCookie("i6t-position");

    // If the cookie isn't set, reset the position to 0
    // and return that.
    if (!cookieString) {
        setPosition(0);
        return 0;
    }

    return parseInt(cookieString);
}

function resetTheWorld() {
    const i6tMainDiv = document.getElementById("i6t-main");
    const actionButton = document.getElementById("i6t-action");

    document.cookie = "i6t-name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    document.cookie = "i6t-position=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

    i6tMainDiv.innerHTML = "Cookies cleared!";
    actionButton.style.display = "none";

    window.location.reload();
}

function loadIframe() {
    const i6tBannerDiv = document.getElementById("i6t-banner");
    const i6tMainDiv = document.getElementById("i6t-main");
    const i6tName = getCookie("i6t-name");
    const actionButton = document.getElementById("i6t-action");
    const queryParams = new URLSearchParams(window.location.search);
    let doRedirect = false;

    if (!i6tName) {
        i6tMainDiv.innerHTML = `
            <p><span style="red">Error: Name not set!</span></p>
            <p>Please refresh the page and enter your name.</p>
        `;
        return;
    }

    // Do we have an icp_name query parameters?
    const icpName = queryParams.get("icp_name");

    // If we have icp_name, it needs to match i6tName.
    if (icpName && icpName !== i6tName) {
        i6tMainDiv.innerHTML = `
            <p><span style="red">Error: Name mismatch!</span></p>
            <p>Please refresh the page and try again.</p>
        `;
        return
    }

    let i6tPosition = getPosition();

    // Do we have an icp_i6t_completed query parameter?
    const icpi6tCompleted = queryParams.get("icp_i6t_completed");

    // If we have icp_i6t_completed...
    if (icpi6tCompleted) {
        // ...then update i6tPosition to be the track after that...
        i6tcompleted = parseInt(icpi6tCompleted);
        i6tPosition = i6tcompleted + 1;
        setPosition(i6tPosition);

        // ...and remember that we should do a redirect.
        doRedirect = true;
    }

    // If i6tPosition is negative, that's an error.
    if (i6tPosition < 0) {
        i6tMainDiv.innerHTML = `
            <p><span style="red">Error: Negative position!</span></p>
            <p>Please refresh the page and try again.</p>
        `;
        return;
    }

    // If i6tPosition is greater than the number of tracks, that's an error.
    if (i6tPosition >= tracks.length) {
        i6tMainDiv.innerHTML = `
            <p><span style="red">Error: Invalid position!</span></p>
            <p>Please refresh the page and try again.</p>
        `;
        return;
    }

    // Use i6t-position to look up which course page to show
    // and fill in the "i6t-main" div with the iframe to the course
    const trackInfo = tracks[i6tPosition];

    if (trackInfo.done) {
        i6tBannerDiv.innerHTML = "<h2>Congratulations!</h2>";
        i6tMainDiv.innerHTML = `
            <p>Congratulations, ${i6tName}! You've completed all the tracks!</p>
        `;

        actionButton.textContent = "Reset and start over";
        actionButton.addEventListener("click", resetTheWorld);
        actionButton.style.display = "block";

        // If we're redirecting - meaning we got here off a finish button -
        // immediately redirect the toplevel window to our own URL.
        if (doRedirect) {
            const redirectTarget = new URL(window.location.href);

            // Make sure we don't get stuck in a loop here.
            redirectTarget.searchParams.delete("icp_name");
            redirectTarget.searchParams.delete("icp_i6t_completed");

            console.log(`Redirecting top to ${redirectTarget.toString()}`);
            window.top.location.replace(redirectTarget.toString());
        }

        return;
    }

    i6tBannerDiv.innerHTML = `<h2>Hi ${i6tName}!</h2>`
    // i6tBannerDiv.innerHTML += `<p>You're on track ${i6tPosition} of ${tracks.length - 1}.</p>`;

    i6tMainDiv.innerHTML = `
        <p>Loading from ${trackInfo.slug}...</p>
    `;

    const finishURL = new URL(`${window.location.origin}/sm101.html`);
    finishURL.searchParams.append("icp_name", i6tName);
    finishURL.searchParams.append("icp_i6t_completed", i6tPosition.toString())

    const trackSlug = trackInfo.slug;
    const baseFrameURL = `https://play.instruqt.com/embed/buoyant/tracks/${trackSlug}`;
    const frameURL = new URL(baseFrameURL);

    let buttonLabel = "Continue";

    if (trackInfo.button) {
        buttonLabel = trackInfo.button;
    }

    frameURL.searchParams.append("token", trackInfo.token);
    frameURL.searchParams.append("icp_name", i6tName);
    frameURL.searchParams.append("finish_btn_target", "_self");
    frameURL.searchParams.append("finish_btn_text", buttonLabel);
    frameURL.searchParams.append("finish_btn_url", finishURL.toString());

    if (doRedirect) {
        console.log(`Redirecting to ${frameURL.toString()}`);
        window.location.href = frameURL.toString();
        return;
    }

    frame = document.createElement("iframe");
    frame.width = "1024px";
    frame.height = "768px";
    frame.style.border = "0";
    frame.allowfullscreen = true;
    frame.sandbox = "allow-forms allow-modals allow-popups allow-same-origin allow-scripts allow-top-navigation";
    frame.src = frameURL.toString();

    i6tMainDiv.innerHTML = "";
    i6tMainDiv.appendChild(frame);

    actionButton.textContent = "Reset and start over";
    // actionButton.addEventListener("click", function () {
    //     setPosition(i6tPosition + 1);
    //     loadIframe();
    // });
    actionButton.addEventListener("click", resetTheWorld);
    actionButton.style.display = "block";
}

function prepPage() {
    // This will get called when the page loads. We need to look for two
    // cookies:
    //
    // First, if i6t-name isn't set, we need to prompt the user for their name
    // by displaying a form in the div with ID "i6t-main". We'll use the form
    // response to set the i6t-name cookie.
    //
    // As long as i6t-name is set, we'll check for i6t-position. If it's not
    // set, we'll force it to "0". Then we'll use i6t-position to look up which
    // course page to show, and fill in the "i6t-main" div with the iframe to
    // the course.

    const i6tBannerDiv = document.getElementById("i6t-banner");
    const i6tMainDiv = document.getElementById("i6t-main");
    const i6tName = getCookie("i6t-name");

    if (!i6tName) {
        const nameForm = document.createElement("form");
        nameForm.innerHTML = `
            <label for="name">Enter your name:</label>
            <input type="text" id="name" name="name">
            <button type="submit">Submit</button>
        `;

        nameForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const nameInput = document.getElementById("name");
            const name = nameInput.value;
            setCookie("i6t-name", name, 365);
            i6tMainDiv.innerHTML = "Thanks! Onward...";
            // Call the function to continue the page preparation
            loadIframe();
        });

        i6tBannerDiv.innerHTML = "<h2>Welcome to our course!</h2>";
        i6tMainDiv.appendChild(nameForm);
    } else {
        loadIframe();
    }
}

window.addEventListener("load", prepPage);