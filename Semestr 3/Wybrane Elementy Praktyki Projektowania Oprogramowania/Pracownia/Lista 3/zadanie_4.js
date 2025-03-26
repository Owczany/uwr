function sum() {
    let acc = 0

    for ( let i = 0; i < arguments.length; i++) {
        acc += arguments[i]
    }

    return acc
}

console.log( sum(1, 2, 3) );

console.log( sum(1, 2, 3, 4, 5) )

console.log( sum(1, 2, 3, 4, 5, 23, 17, 8) )