var http = require('http')

const PORT = 3000

http.createServer((req, res) => {
    res.setHeader('Content-type', 'text/html; charset=utf-8')
    res.end(`Cześć Świecie: ${req.url}, it's ${new Date()}`)
}).listen(PORT)

console.log(`Server started on port: ${PORT}`)