function* take(it, top) {
    let n = 0
    for (var _result; _result = it.next(), n < top; n++) {
        console.log(_result.value)
    }
}

function* fib() {
    let current, next = 0, future = 1
    while (true) {
        current = next
        next = future
        future = next + current
        yield current
    }
}

for (let num of take(fib(), 10)) {
    console.log(num)
}