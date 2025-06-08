const btn = document.querySelector("button");
const OFFSET = 100;

const testEdge = function (property, axis) {
if (endPoint[property] <= 0) {
    endPoint[property] = axis - OFFSET;
} else if (endPoint[property] >= axis) {
    endPoint[property] = OFFSET;
}
};

let endPoint = { x: innerWidth / 2, y: innerHeight * 2 / 3 };

addEventListener("mousemove", (e) => {
const btnRect = btn.getBoundingClientRect();

const angle = Math.atan2(e.y - endPoint.y, e.x - endPoint.x);

const distance = Math.sqrt(
    Math.pow(e.x - endPoint.x, 2) + Math.pow(e.y - endPoint.y, 2)
);

if (distance <= OFFSET) {
    endPoint = {
    x: OFFSET * -Math.cos(angle) + e.x,
    y: OFFSET * -Math.sin(angle) + e.y
    };
}

btn.style.left = endPoint.x + "px";
btn.style.top = endPoint.y + "px";

btn.disabled = true;

testEdge("x", innerWidth);
testEdge("y", innerHeight);
});



// Select all pupils
const pupils = document.querySelectorAll('.pupil');

// Add an event listener for mouse movement
document.addEventListener('mousemove', (event) => {
    const { clientX: mouseX, clientY: mouseY } = event;

    // Adjust each pupil position
    pupils.forEach((pupil) => {
        const eye = pupil.parentElement;

        // Get the bounding box of the eye
        const { left, top, width, height } = eye.getBoundingClientRect();

        // Calculate the center of the eye
        const eyeCenterX = left + width / 2;
        const eyeCenterY = top + height / 2;

        // Calculate the offset for the pupil based on the eye center
        const dx = mouseX - eyeCenterX;
        const dy = mouseY - eyeCenterY;

        // Normalize the movement within a range
        const maxOffsetX = width * 0.25; // Adjust range for horizontal movement
        const maxOffsetY = height * 0.25; // Adjust range for vertical movement

        const offsetX = Math.max(-maxOffsetX, Math.min(maxOffsetX, dx * 0.1));
        const offsetY = Math.max(-maxOffsetY, Math.min(maxOffsetY, dy * 0.1));

        // Set the pupil position
        pupil.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
    });
});

