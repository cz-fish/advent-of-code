const d09 = require("./09.js");
const d10 = require("./10.js");
const d11 = require("./11.js");
const d12 = require("./12.js");
const d13 = require("./13.js");

const dayMap = {
    9: d09.run,
    10: d10.run,
    11: d11.run,
    12: d12.run,
    13: d13.run,
};

process.argv.forEach(arg => {
    const num = parseInt(arg);
    if (dayMap[num]) {
        console.log(`Running day ${num}`);
        dayMap[num]();
    }
});
