console.log( (![]+[])[+[]] + (![]+[])[+!+[]] + ([![]]+[][[]])[+!+[]+[+[]]] + (![]+[])[!+[]+!+[]] );

// Część pierwsza
// ![]+[])[+[]]
console.log()
console.log( ![] )
console.log( typeof(![]) )

console.log( +[] )
console.log( typeof(+[]) )

console.log( ![]+[] )
console.log( typeof(![]+[]) )

console.log( +[] )
console.log( typeof(+[]) )

console.log( (![]+[])[+[]] )
console.log( typeof((![]+[])[+[]]) )

console.log('---------')

// Część druga
// (![]+[])[+!+[]]
console.log( ![] )
console.log( typeof(![]) )

console.log( +[] )
console.log( typeof(+[]) )

console.log( ![]+[] )
console.log( typeof(![]+[]) )

console.log( +[] )
console.log( typeof(+[]) )

console.log( !+[] )
console.log( typeof(!+[]) )

console.log( +!+[] )
console.log( typeof(+!+[]) )

console.log( (![]+[])[+!+[]] )
console.log( typeof((![]+[])[+!+[]]) )

console.log('---------')
// Część trzecia
// ([![]]+[][[]])[+!+[]+[+[]]]
console.log( ![] )

console.log( [![]] )

console.log( +[] )

console.log( [![]]+[] )

console.log( [[]] )

console.log( [![]]+[][[]] )

console.log( [+!+[]+[+[]]] )

console.log( ([![]]+[][[]])[+!+[]+[+[]]] )

console.log('---------')

// Część czwarta
// (![]+[])[!+[]+!+[]]

console.log( ![]+[] )
console.log( typeof(![]+[]) )

console.log( !+[]+!+[] )
console.log( typeof(!+[]+!+[]) )

console.log( (![]+[])[!+[]+!+[]] )
console.log( typeof((![]+[])[!+[]+!+[]]) )


console.log('Podsumowanie ')