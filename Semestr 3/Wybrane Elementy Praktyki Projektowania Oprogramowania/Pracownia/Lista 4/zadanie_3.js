var Person = function(name) {
    this.name = name;
}

Person.prototype.say = function() {
    return `Nazywam się ${this.name}`;
}

var Worker = function(name, age) {
    Person.call( this, name );
    this.age = age;
}

// Dobra wersja
Worker.prototype = Object.create( Person.prototype ) // Tak powinno się robić

// Zła wersja 1
// Worker.prototype = Person.prototype; // Tutaj nadpisujemy funkcje dla Person równiez

// Zła wersja 2
// Worker.prototype = new Person(); // Tutaj brak oszczędności pamięci

Worker.prototype.say = function() {
    return `Nazywam się ${this.name} i mam ${this.age} lat`
}

// Testy
var w = new Worker('Piotr', 20);
console.log( w.say() )

var p = new Person('Adam')
console.log( p.say() )