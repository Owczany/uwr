function forEach<T>(a: T[], f: (t: T, i: number, a: T[]) => void): void {
    for (let i = 0; i < a.length; i++) {
        f(a[i], i, a);
    }
}

function map<T>(a: T[], f: (t: T, i: number, a: T[]) => T): T[] {
    const result = [];
    for (let i = 0; i < a.length; i++) {
        result.push(f(a[i], i, a));
    }
    return result;
}

function filter<T>(a: T[], f: (t: T, i: number, a: T[]) => boolean): T[] {
    const result: T[] = [];
    for (let i = 0; i < a.length; i++) {
        if (f(a[i], i, a)) {
            result.push(a[i]);
        }
    }
    return result;
}

// Przykłady użycia
var a = [1, 2, 3, 4];

// forEach z funkcją strzałkową
forEach(a, _ => { console.log(_) }); // Wypisuje: 1, 2, 3, 4

// filter z funkcją strzałkową
console.log(filter(a, _ => _ < 3)); // Wypisuje: [1, 2]

// map z funkcją strzałkową
console.log(map(a, _ => _ * 2)); // Wypisuje: [2, 4, 6, 8]

// Użycie z funkcjami tradycyjnymi
forEach(a, function(value) { console.log(value); }); // Wypisuje: 1, 2, 3, 4
console.log(filter(a, function(value) { return value < 3; })); // Wypisuje: [1, 2]
console.log(map(a, function(value) { return value * 2; })); // Wypisuje: [2, 4, 6, 8]
