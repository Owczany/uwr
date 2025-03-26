const readline = require('readline')
const fs = require('fs')

// Część pierwsza czytanie pliku
const filePath = 'serwer.txt'

// const rl = readline.createInterface(fs.createReadStream(filePath), process.stdout);

// Część druga

function callculate(filePath) {
    const rl = readline.createInterface(fs.createReadStream(filePath), process.stdout);
    let users = {}
    rl.on('line', (line) => {

        if (users[line.split(' ')[1]] === undefined) {
            users[line.split(' ')[1]] = 1
        } else {
            users[line.split(' ')[1]] += 1
        }
    })

    rl.on('close', () => {
        const num = [0, 0, 0]
        const rank = ['', '', '']
        for (let user in users) {
            if (users[user] > num[0]) {
                num[2] = num[1]
                num[1] = num[0]
                num[0] = users[user]
                rank[2] = rank[1]
                rank[1] = rank[0]
                rank[0] = user
            } else if (users[user] > num[1]) {
                num[2] = num[1]
                num[1] = users[user]
                rank[2] = rank[1]
                rank[1] = user
            } else if (users[user] > num[2]) {
                num[2] = users[user]
                rank[2] = user
            }
        }
        console.log(users)
        for (let i = 0; i < num.length ; i++)
        console.log(`${rank[i]}: ${num[i]}`)
    })
}

callculate(filePath)