function fib_rec(n: number): number {
    if (n === 0) {
        return 0;
    }
    if (n === 1) {
        return 1;
    }

    return fib_rec(n - 1) + fib_rec(n - 2);
}

console.log(fib_rec(40));

function fib_memo(n: number): number {
    let cache: { [key: number]: number } = { 0: 0, 1: 1 };

    function fib(n: number): number {
        if (n in cache) {
            return cache[n];
        }
        let res = fib(n - 1) + fib(n - 2);
        cache[n] = res;
        return res;
    }

    return fib(n);
}

console.log(fib_memo(100));

var fib = function (n: number): number {
    if (n === 0) {
        return 0;
    }
    if (n === 1) {
        return 1;
    }

    return fib(n - 1) + fib(n - 2)
}

function memo<T extends number | string, U>(f: (n: T) => U): (n: T) => U ) {
    let cache: { [key: T]: U } = {}

    return function (n) {
        if (n in cache) {
            return cache[n]
        } else {
            let res = f(n)
            cache[n] = res
            return res
        }
    }
}



fib = memo(fib)

console.log(fib(10));
console.log(fib(100));
