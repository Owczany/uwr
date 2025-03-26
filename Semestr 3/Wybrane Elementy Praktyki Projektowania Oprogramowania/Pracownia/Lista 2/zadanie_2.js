// Pierwsza część
let person = {
    name: 'Piotr',
    age: 20,
    "a a" :  'Tutaj coś jest nie tak',
    1: 'Jeden',
    '[object Object]': 'Objekt?'
}

// Pokazujemy, ze da się dostać do włąściwości / pola obiektu
console.log( person.name )
console.log( person['name'] )

// Po kropce zawsze jest utrzymywana konwencja (nie ma spacji oraz nie zaczyna sie od liczb)
// console.log( person.a a )
console.log( person["a a"] )

// Druga część
console.log( person[1] ) // Konwertuje na stringa

let obj = { a: 1 }
console.log( person[obj] ) // obj parsuje od stringa [object Object]

// Programista ma duze mozliwości związane z taki rozwiązaniem, jednka klucze zawsze sa konwertowane do stringa

// Część trzecia
let arr = [1, 2, 3]
arr["name"] = 'Czy tutaj jest Albert?'
console.log( arr["name"] ) // Oznacz to, ze Array tez jest obiektem

arr[obj] = "To nie moze sie udac"
console.log( arr[obj] )

console.log( arr )

console.log( arr.length ) // Dodawanie wlasciwosci nie wplywa na dlugosc tablicy

arr.length = 10
console.log( arr )

arr.length = 1
console.log( arr )
