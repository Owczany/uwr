function Foo() {
    function Qux() {
        console.log("Foo::Qux - funkcja prywatna");
    }

    // this.Bar = function() {
    //     console.log("Foo::Bar - funkcja publiczna");
    //     Qux();
    // };
}

Object.prototype.Bar = (function() {
    function Qux() {
        console.log("Foo::Qux - funkcja prywatna");
    }
    return function() {
        console.log('BAr')
        Qux()
    }})();
    



let foo = new Foo();
foo.Bar(); 

// foo.Qux(); 
