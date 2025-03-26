const fs = require('node:fs');

// Za pomocą call backa
fs.readFile('./text.txt', 'utf8', (err, data) => {
    if (err) {
        console.error(err);
        return;
    }
    console.log(data);
});

// Za pomocą promise 

(async function example() {
  try {
    const data = await fs.promises.readFile('./text.txt', { encoding: 'utf8' });
    console.log(data);
  } catch (err) {
    console.log(err);
  }
})()
