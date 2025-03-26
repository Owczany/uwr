function createGenerator(n) {
    var _state = 0;
    return function() {
        return {
            next : function() {
                return {
                    value : _state,
                    done : _state++ >= n
                }
            }
        }
    }
}

var foo1 = {
    [Symbol.iterator] : createGenerator(5)
}

var foo2 = {
    [Symbol.iterator] : createGenerator(20)
}

for (var f of foo1) {
    console.log(f)
}

for (var f of foo2) {
    console.log(f)
}
