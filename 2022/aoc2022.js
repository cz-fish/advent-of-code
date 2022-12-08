const d08 = require("./08.js");

const dayMap = {
    8: d08.run,
};

process.argv.forEach(arg => {
    const num = parseInt(arg);
    if (dayMap[num]) {
        console.log(`Running day ${num}`);
        dayMap[num]();
    }
});
