var http = require('http');
var express = require('express');
const { type } = require('os');

app = express();

app.set('view engine', 'ejs');
app.set('views', './views');

app.use(express.urlencoded({ extended: true }));

// Strona główna - formularz
app.get('/', (req, res) => {
    res.render('index', {
        firstName: "",
        lastName: "",
        course: "",
        tasks: Array(10).fill(""),
        message: null
    });
});

// Obsługa przesłania formularza
app.post('/', (req, res) => {
    const { firstName, lastName, course, ...tasks } = req.body;

    console.log(typeof tasks) // object

    if (!firstName || !lastName || !course) {
        // Zwróć formularz z błędem
        res.render('index', {
            firstName,
            lastName,
            course,
            tasks: Object.values(tasks),
            message: "Imię, nazwisko i nazwa zajęć są wymagane!"
        });
    } else {
        // Przekaż dane do widoku wydruku
        const taskPoints = Object.keys(tasks).map((key) => ({
            task: key.replace("task", ""),
            points: tasks[key] ? parseInt(tasks[key], 10) : 0
        }));
        res.redirect(
            `/print?firstName=${firstName}&lastName=${lastName}&course=${course}&tasks=${encodeURIComponent(JSON.stringify(taskPoints))}`
        );
    }
});

// Widok wydruku
app.get('/print', (req, res) => {
    const { firstName, lastName, course, tasks } = req.query;

    // console.log(typeof tasks) // string
    // console.log(typeof firstName) // string

    const taskPoints = JSON.parse(tasks);
    res.render('print', {
        firstName,
        lastName,
        course,
        tasks: taskPoints
    });
});

// Uruchomienie serwera
http.createServer(app).listen(3000);
console.log('Server Started');
