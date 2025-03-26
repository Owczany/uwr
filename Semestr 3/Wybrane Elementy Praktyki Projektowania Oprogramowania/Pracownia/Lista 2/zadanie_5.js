let person = {
    name: 'Piotr',
    
    sayMyName() {
        return 'Hello my name is ' + this.name;
    },

    get age() {
        return this._age
    },

    set age(value) {
        this._age = value
    },
};

person.age = 20

console.log(person.sayMyName())
console.log(person.age)

person.surrname = 'Pijanowski'

person.sayMySurrname = function() {
    return "My last name is " + this.surrname
}

console.log(person.sayMySurrname())

Object.defineProperty(person, 'fullName', {
    get() {
        return this.name + " "  +this.surrname;
    },
    set(value) {
        let a = value.split(' ')
        this.name = a[0]
        this.surrname = a[1]
    }
})

console.log(person.fullName)

person.fullName = 'Adam Kowalski'

console.log(person.fullName)

// Wlasciwosci musza byc definiowane za pomoca define property


