readln = require('readline')

var cl = readln.createInterface(process.stdin, process.stdout);
var question = function (q) {
    return new Promise((res, rej) => {
        cl.question(q, answer => {
            res(answer);
        })
    });
};

const liczba = Math.floor(Math.random() * 100) + 1;

(async function main() {
    var answer;
    while (parseInt(answer, 10) != liczba) {
        answer = await question('Zgadnij liczbę: ');
        if (parseInt(answer, 10) > liczba) {
            console.log('Liczba jest mnniejsza')
        } else if (parseInt(answer, 10) < liczba) {
            console.log('Liczba jest większa')
        }
    }
    console.log('Tak trafiłeś!');
    cl.close()
})();
