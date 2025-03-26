"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.persons = void 0;
exports.isAdmin = isAdmin;
exports.isUser = isUser;
exports.logPerson = logPerson;
exports.persons = [
    {
        type: 'user',
        name: 'Jan Kowalski',
        age: 17,
        occupation: 'Student'
    },
    {
        type: 'admin',
        name: 'Tomasz Malinowski',
        age: 20,
        role: 'Administrator'
    }
];
function isAdmin(person) {
    return person.type === 'admin';
}
function isUser(person) {
    return person.type === 'user';
}
function logPerson(person) {
    var additionalInformation = '';
    if (isAdmin(person)) {
        additionalInformation = person.role;
    }
    if (isUser(person)) {
        additionalInformation = person.occupation;
    }
    console.log(" - ".concat(person.name, ", ").concat(person.age, ", ").concat(additionalInformation));
}
for (var _i = 0, persons_1 = exports.persons; _i < persons_1.length; _i++) {
    var person = persons_1[_i];
    logPerson(person);
}
