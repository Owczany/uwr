function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function fib1() {
    let next = 0, future = 1
    return {
        next : function() {
            let current = next
            next = future
            future = current + next
            return {
                value : current,
                done : false
            }
        },
        // [Symbol.iterator] : fib1 // bez tego nie da sie wywolac for of
    }
}

function* fib2() {
    let current, next = 0, future = 1
    while (true) {
        current = next
        next = future
        future = next + current
        yield current
    }
}

// var _it1 = fib1();
// for ( var _result; _result = _it1.next(), !_result.done; ) {
//     console.log(_result.value)
//     await delay(250)
// }

// var _it2 = fib2();
// for ( var _result; _result = _it2.next(), !_result.done; ) {
//     console.log(_result.value)
//     await delay(250)
// }

// Dlatego nie działa, bo to iterator ale da sie to naprawić
for (var f of fib1()) {
    console.log(f)
    await delay(250)
}

// for (var f of fib2()) {
//     console.log(f)
//     await delay(250)
// }
