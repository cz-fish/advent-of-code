const images = {};
const canvas = document.getElementById("screen");
const ctx = canvas.getContext('2d');
const width = 1024;
const height = 768;
const img_w = 560;
const img_h = 800;

function wait_for_images()
{
    const names = ["base"];
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
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, width, height);
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
        const x = 620;
        const y = 250;
        const radius = 20;
        const w = 100;
        const h = 50;

        const r = x + w;
        const b = y + h;
        ctx.beginPath();
        ctx.strokeStyle="black";
        ctx.lineWidth="2";
        ctx.moveTo(x+radius, y);
        ctx.lineTo(x+radius/2, y-10);
        ctx.lineTo(x+radius * 2, y);
        ctx.lineTo(r-radius, y);
        ctx.quadraticCurveTo(r, y, r, y+radius);
        ctx.lineTo(r, y+h-radius);
        ctx.quadraticCurveTo(r, b, r-radius, b);
        ctx.lineTo(x+radius, b);
        ctx.quadraticCurveTo(x, b, x, b-radius);
        ctx.lineTo(x, y+radius);
        ctx.quadraticCurveTo(x, y, x+radius, y);
        ctx.stroke();

        ctx.textAligh = "center";
        ctx.fillStyle = "black";
        ctx.font = "30px Arial";
        ctx.fillText("" + state.number, x + 30, y + 35);
    }

    state.phase += 5;

    window.requestAnimationFrame(draw);
    //window.setTimeout(draw, 1500);
}

wait_for_images();
