const https = require('node:https');

function fetchData(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = ''

            res.on('data', (chunk) => {
                data += chunk
            })

            res.on('end', () => {
                resolve(data)
            })
        }).on('error', (e) => {
            reject(e)
        })
    });
}

// fetchData('https://www.youtube.com/').then((content) => console.log(content)).catch((err) => console.log(err))

(async () => {
    try {
        const data = await fetchData('https://www.google.com/')
        console.log(data)

    } catch (err) {
        console.log(err)
    }
})()
