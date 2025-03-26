function fib_rec(n) {
    if (n === 0) {
        return 0;
    }
    if (n === 1) {
        return 1;
    }
    return fib_rec(n - 1) + fib_rec(n - 2);
}
console.log(fib_rec(40));
function fib_memo(n) {
    var cache = { 0: 0, 1: 1 };
    function fib(n) {
        if (n in cache) {
            return cache[n];
        }
        var res = fib(n - 1) + fib(n - 2);
        cache[n] = res;
        return res;
    }
    return fib(n);
}
console.log(fib_memo(100));
var fib = function (n) {
    if (n === 0) {
        return 0;
    }
    if (n === 1) {
        return 1;
    }
    return fib(n - 1) + fib(n - 2);
};
function memo(f) {
    var cache = {};
    return function (n) {
        if (n in cache) {
            return cache[n];
        }
        else {
            var res = f(n);
            cache[n] = res;
            return res;
        }
    };
}
fib = memo(fib);
console.log(fib(10)); // 55
console.log(fib(100)); // 12586269025
