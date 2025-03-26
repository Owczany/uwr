var p = { name: 'jan' };
var q = { surname: 'kowalski' };
Object.setPrototypeOf(p, q);

function isOwnProperty(obj, prop) {
    return obj.hasOwnProperty(prop);
}

console.log(isOwnProperty(p, 'name')); // true
console.log(isOwnProperty(p, 'surname')); // false

console.log("Własne właściwości obiektu p:");
for (let key in p) {
    if (p.hasOwnProperty(key)) {
        console.log(key);
    }
}

console.log("Wszystkie właściwości obiektu p (w tym z prototypów):");
for (let key in p) {
    console.log(key);
}
