var https = require('https');
var fs = require('fs');

(async function () {

    var pfx = await fs.promises.readFile('Klucze i Certyfikaty/certificate.pfx');
    https.createServer(
        {
            pfx: pfx,
            passphrase: 'password'
        },
        (req, res) => {
            res.setHeader('Content-type', 'text/html; charset=utf-8')
            res.end(`Cześć Świecie: ${req.url}, it's ${new Date()}`)
        }).listen(3000, () => {
            console.log('Server started')
        });

})();
