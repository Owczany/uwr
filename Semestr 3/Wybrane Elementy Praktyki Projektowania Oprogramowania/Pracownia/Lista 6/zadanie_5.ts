type User = {
    type: 'user'; // string tez działa zapytać - juz wiem ;>
    name: string;
    age: number;
    occupation: string;
}

type Admin = {
    type: 'admin'; // string tez działa zapytać - juz wiem ;>
    name: string;
    age: number;
    role: string;
}

export type Person = User | Admin;

export const persons: Person[] = [
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

export function isAdmin(person: Person)/*: person is Admin */{
    return person.type === 'admin';
}

export function isUser(person: Person)/*: person is User */{
    return person.type === 'user';
}


export function logPerson(person: Person) {
    let additionalInformation: string = '';
    if (isAdmin(person)) {
        additionalInformation = person.role;
    }
    if (isUser(person)) {
        additionalInformation = person.occupation;
    }
    console.log(` - ${ person.name }, ${ person.age }, ${ additionalInformation }`);
}

for (let person of persons) {
    logPerson(person)
}
