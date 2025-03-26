// Drzewo binarne z prototype
function Tree(val, left, right) {
    this.left = left;
    this.right = right;
    this.val = val;
}

Tree.prototype[Symbol.iterator] = function*() {
    const queue = [this]
    while (queue.length > 0) {
        // let node = queue.shift()
        let node = queue[0]
        // queue = queue.slice(1) // tu musimy uyc leta
        queue.splice(0, 1)
        
        yield node.val

        if (node.left) {queue.push(node.left)}
        if (node.right) {queue.push(node.right)}
    }
}

var root = new Tree( 1,
new Tree( 2, new Tree( 3 ) ), new Tree( 4 ));
for ( var e of root ) {
    console.log( e );
}
