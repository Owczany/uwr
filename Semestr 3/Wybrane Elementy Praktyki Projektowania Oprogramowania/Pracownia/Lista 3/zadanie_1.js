// fib rekurencyjnie bez memoizacji
function fib_rec(n) {
    if (n === 0) {
        return 0
    }

    if (n === 1) {
        return 1
    }

    return fib_rec(n - 1) + fib_rec(n - 2)
}

// fib iteracyjnie
function fib_itr(n) {
    if (n === 0) {
       return 0;
    }
 
    if (n === 1) {
       return 1;
    }
 
    let sum = 0
    let p1 = 1
    let p2 = 0
 
    for (let i = 2; i <= n; i++) {
       sum = p1 + p2
       p2 = p1
       p1 = sum
    }
 
    return sum
 }

// fib rekurencyjnie z memoizacja #MOJA WERSJA#
function fib_memo(n) {
    let memo = {}

    function fib(n) {
        if (n === 0) {
            return 0
        }
        
        if (n === 1) {
            return 1
        }

        if (memo[n] !== undefined) {
            return memo[n]
        } else {
            res = fib(n - 1) + fib(n - 2)
            memo[n] = res
            return res
        }
    }

    return fib(n)
}

// fib rekurencyjnie z memoizacja wersja z wykladu
function fib1(n) {
    if (n === 0) {
        return 0
    }

    if (n === 1) {//guwno
        return 1
    }

    return fib1(n - 1) + fib1(n - 2)
}

function memo(f) {
    let cache = {}

    return function(n) {
        if (cache[n] !== undefined) {
            return cache[n]
        } else {
            res = f(n)
            cache[n] = res
            return res
        }
    }
}

var fib1 = memo(fib1) // Tu musimy uzyc var bo chcemy, zeby zmienna var byla wczesniej zdefiniowana

console.time('RecFib');
console.log(fib_rec(40));
console.timeEnd('RecFib');
console.time('IterFib');
console.log(fib_itr(40));
console.timeEnd('IterFib');
console.time('MemoFib')
console.log(fib1(40))
console.timeEnd('MemoFib')
console.time('MyMemoFib')
console.log(fib_memo(40))
console.timeEnd('MyMemoFib')
