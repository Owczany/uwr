function getLastProto(o) {
    var p = o;
    do {
        o = p;
        p = Object.getPrototypeOf(o);
        console.log(`${p} objekt`)
    } while (p);

    return o
}

var p = {}
var q = {}
var r = {}
var s = {}

Object.setPrototypeOf(p, q)
Object.setPrototypeOf(p, r)
Object.setPrototypeOf(s, String)

// console.log(getLastProto(p))
// console.log(getLastProto(q))
// console.log(getLastProto(r))
console.log(getLastProto(s))

