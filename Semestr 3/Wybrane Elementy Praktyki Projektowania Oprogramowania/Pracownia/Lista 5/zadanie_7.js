const fs = require('fs');

// Klasyczny sposób użycia fs.readFile z funkcją zwrotną (callback)
// fs.readFile('example.txt', 'utf8', (err, data) => {
//     if (err) {
//         console.error('Błąd podczas odczytu pliku:', err);
//     } else {
//         console.log('Zawartość pliku (callback):', data);
//     }
// });



// Ręcznie 
// function readFilePromise(url) {
//     return new Promise((resolve, reject) => {
//         fs.readFile(url, 'utf-8', (err, data) => {
//             if (err) {
//                 reject(err)
//             } else {
//                 resolve(data)
//             }
//         });
//     });
// }

// Stary sposób
// readFilePromise('example.txt').then((content) => {
//     console.log(content)
// }).catch((err) => {
//     console.log(err)
// })

// Nowy sposób
// (async () => {
//     try {
//         var data = await readFilePromise('example.txt')
//         console.log(data)
//     } catch (error) {
//         console.log(error)
//     }
// })()

// util
const util = require('util');
const readFilePromisified = util.promisify(fs.readFile);

// Stary sposób
// readFilePromisified('example.txt', 'utf-8').then((content) => {
//     console.log(content)
// }).catch((e) => {
//     console.log(e)
// })

// Nowy sposób
// (async () => {
//     try {
//         const data = await readFilePromisified('example.txt', 'utf-8');
//         console.log('Zawartość pliku (promisify):', data);
//     } catch (err) {
//         console.error('Błąd (promisify):', err);
//     }
// })();

// fs.promises

(async () => {
    try {
        const data = await fs.promises.readFile('example.txt', 'utf-8')
        console.log(data)
    } catch (error) {
        console.log(error)
    }
})()

// fs.promises.readFile('example.txt', 'utf-8').then((content) => {
//     try {
//         console.log(content)
//     } catch (error) {
//         console.log(error)
//     }
// })
console.log('adas')
