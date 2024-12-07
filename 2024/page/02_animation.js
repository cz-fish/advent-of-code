const images = {};
const canvas = document.getElementById("screen");
const ctx = canvas.getContext('2d');
const width = 1024;
const height = 768;
const img_w = 560;
const img_h = 800;

function wait_for_images()
{
    const names = ["base", "scene"];
    for (const index of [1, 2, 3, 4, 5, 6]) {
        for (const type of ["hat", "outfit", "shoes"]) {
            names.push(type + index);
        }
    }
    for (const img of names) {
        if (!document.getElementById(img).complete) {
            window.setTimeout(wait_for_images, 50);
            return;
        }
        images[img] = document.getElementById(img);
    }
    window.requestAnimationFrame(draw);
}

const max_phase = 400;
const state = {
    number: 0,
    hat: undefined,
    outfit: undefined,
    shoes: undefined,
    phase: max_phase,
};

function draw()
{
    ctx.clearRect(0, 0, width, height);
    ctx.drawImage(images["scene"], 0, 0, width, height);
    const left = (width - img_w) / 2;
    const top = (height - img_h) / 2;
    ctx.drawImage(images["base"], left, top, img_w, img_h);

    if (state.phase >= max_phase) {
        const choice = Math.floor(Math.random() * 6 * 6 * 6);
        state.number = choice;
        state.hat = "hat" + (choice % 6 + 1);
        state.outfit = "outfit" + (Math.floor(choice / 6) % 6 + 1);
        state.shoes = "shoes" + (Math.floor(choice / 36) + 1);
        state.phase = 0;
        console.log(state);
    }

    let range = 0;
    let speechBubble = false;
    if (state.phase < max_phase / 4) {
        range = 1 - state.phase / (max_phase / 4);
    } else if (state.phase < 3 * max_phase / 4) {
        speechBubble = true;
    } else {
        range = (state.phase - 3 * max_phase / 4) / (max_phase / 4);
    }
    const shoes_l = left - 200 * range;
    const shoes_t = top + 150 * range;
    const outfit_l = left + 600 * range;
    const outfit_t = top + 50 * range;
    const hat_l = left + 120 * range;
    const hat_t = top - 400 * range;

    ctx.drawImage(images[state.shoes], shoes_l, shoes_t, img_w, img_h);
    ctx.drawImage(images[state.outfit], outfit_l, outfit_t, img_w, img_h);
    ctx.drawImage(images[state.hat], hat_l, hat_t, img_w, img_h);

    if (speechBubble) {
        drawBubble("" + state.number, 640, 280);
    }

    state.phase += 5;

    window.requestAnimationFrame(draw);
}

function drawBubble(text, x, y) {
    ctx.font = "30px Arial";
    const measure = ctx.measureText(text);
    const margin = 20;
    const radius = 20;
    const left = x - measure.width / 2 - margin;
    const right = x + measure.width / 2 + margin;
    const top = y - 15 - margin;
    const bottom = y + margin;

    ctx.strokeStyle = "black";
    ctx.fillStyle = "white";
    ctx.lineWidth="2";
    ctx.beginPath();
    ctx.moveTo(left + radius, top);
    ctx.lineTo(left + radius / 2, top - 10);
    ctx.lineTo(left + radius * 2, top);
    ctx.lineTo(right - radius, top);
    ctx.quadraticCurveTo(right, top, right, top + radius);
    ctx.lineTo(right, bottom - radius);
    ctx.quadraticCurveTo(right, bottom, right - radius, bottom);
    ctx.lineTo(left + radius, bottom);
    ctx.quadraticCurveTo(left, bottom, left, bottom - radius);
    ctx.lineTo(left, top + radius);
    ctx.quadraticCurveTo(left, top, left + radius, top);
    ctx.closePath();
    ctx.stroke();
    ctx.fill();

    ctx.textAlign = "center";
    ctx.fillStyle = "black";
    ctx.fillText(text, x, y);
}

wait_for_images();
