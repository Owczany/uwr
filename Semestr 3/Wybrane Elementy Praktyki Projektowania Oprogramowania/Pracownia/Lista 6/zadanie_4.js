"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.persons = void 0;
exports.persons = [
    {
        name: 'Jan Kowalski',
        age: 17,
        occupation: 'Student'
    },
    {
        name: 'Tomasz Malinowski',
        age: 20,
        role: 'Administrator'
    }
];
function logPerson(person) {
    var additionalInformation;
    if ('role' in person) {
        additionalInformation = person.role;
    }
    else {
        additionalInformation = person.occupation;
    }
    console.log(" - ".concat(person.name, ", ").concat(person.age, ", ").concat(additionalInformation));
}
for (var _i = 0, persons_1 = exports.persons; _i < persons_1.length; _i++) {
    var person = persons_1[_i];
    logPerson(person);
}
