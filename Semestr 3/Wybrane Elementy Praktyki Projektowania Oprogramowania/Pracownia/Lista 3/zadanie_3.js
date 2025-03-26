function createFs(n) {
    var fs = [];
    for (var i = 0; i < n; i++) {
        fs[i] = function () {
            return i
        };
    };
    return fs;
}

function createFsLet(n) {
    var fs = [];
    for (let i = 0; i < n; i++) {
        fs[i] = function () {
            return i
        };
    };
    return fs;
}

function createFsVar(n) {
    var fs = [];
    for (var i = 0; i < n; i++) {
        (function (i) {
            return fs[i] = function () {
                return i
            };
        })(i)
    };
    return fs;
}

var myfs = createFs(10);

console.log(myfs[0]());
console.log(myfs[2]());
console.log(myfs[7]());

var myfslet = createFsLet(10);

console.log(myfslet[0]());
console.log(myfslet[2]());
console.log(myfslet[7]());

var myfsvar = createFsVar(10);

console.log(myfsvar[0]());
console.log(myfsvar[2]());
console.log(myfsvar[7]());
