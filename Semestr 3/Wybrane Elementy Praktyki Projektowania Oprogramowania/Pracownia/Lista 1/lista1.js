// Zadanie 2

// Funkcja wypisująca liczby podzielne przez swoje cyfry i sumę swoich cyfr
function myFunction() {
   const arr = [];

   for (let num = 1; num <= 100000; num++) {
      let isGood = true
      let sum = 0
      for (let digit of String(num)) {
         digit = Number(digit)

         if (digit === 0) {
            continue
         }

         sum += digit

         if (num % digit !== 0) {
            isGood = false
            break
         }
      }

      if (num % sum !== 0) {
         isGood = false
      }

      if (isGood) {
         arr.push(num)
      }
   }
   // arr = []
   return arr
}

console.log(myFunction())


// Zadanie 3

function isPrime(n) {
   for (let i = 2; i < n; i++) {
      if (n % i === 0) {
         return false;
      }
   }

   return true;
}

function primaryNumbers() {
   let arr = [];
   for (let i = 2; i <= 100000; i++) {
      if (isPrime(i)) {
         arr.push(i);
      }
   }

   return arr
}

console.log(primaryNumbers());


// Zadanie 4

/// Debug w chromie F12 w chromie -> Sources -> snippet

/// Debug w visual comand + shift + d

// Zadanie 5

function fibb_rec(n) {
   if (n === 0) {
      return 0;
   }

   if (n === 1) {
      return 1;
   }

   return fibb_rec(n - 1) + fibb_rec(n - 2);
}

function fibb_itr(n) {
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
console.time('RecFib');
console.log(fibb_rec(40));
console.timeEnd('RecFib');
console.time('IterFib');
console.log(fibb_itr(40));
console.timeEnd('IterFib');
