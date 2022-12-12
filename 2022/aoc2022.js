const d08 = require("./08.js");
const d10 = require("./10.js");
const d11 = require("./11.js");

const dayMap = {
    8: d08.run,
    10: d10.run,
    11: d11.run,
};

process.argv.forEach(arg => {
    const num = parseInt(arg);
    if (dayMap[num]) {
        console.log(`Running day ${num}`);
        dayMap[num]();
    }
});
