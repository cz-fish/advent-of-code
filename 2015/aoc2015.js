const d09 = require("./09.js");
const d10 = require("./10.js");
const d11 = require("./11.js");
const d12 = require("./12.js");
const d13 = require("./13.js");
const d14 = require("./14.js");
const d15 = require("./15.js");
const d16 = require("./16.js");
const d17 = require("./17.js");
const d18 = require("./dist/18");

const dayMap = {
    9: d09.run,
    10: d10.run,
    11: d11.run,
    12: d12.run,
    13: d13.run,
    14: d14.run,
    15: d15.run,
    16: d16.run,
    17: d17.run,
    18: d18.run,
};

process.argv.forEach(arg => {
    const num = parseInt(arg);
    if (dayMap[num]) {
        console.log(`Running day ${num}`);
        dayMap[num]();
    }
});
