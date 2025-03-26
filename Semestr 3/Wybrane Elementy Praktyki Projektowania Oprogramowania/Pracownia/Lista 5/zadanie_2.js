readln = require('readline')

var cl = readln.createInterface(process.stdin, process.stdout);
var question = function (q) {
    return new Promise((res, rej) => {
        cl.question(q, answer => {
            res(answer);
        })
    });
};

(async function main() {
    var name;
    name = await question('Cześć, jak się nazywasz? ');

    console.log(`Cześć ${name}, miło Cie widzieć!`);
    cl.close()
})();
