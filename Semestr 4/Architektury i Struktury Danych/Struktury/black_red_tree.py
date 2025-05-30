class Node():
    def __init__(self, value: int, left = None, right = None, parent = None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        if self.left and self.right:
            return f'Node( {self.left.__str__()} {self.value} {self.right.__str__()} )'
        if self.left:
            return f'Node( {self.left.__str__()} {self.value}, Leaf )'
        if self.right:
            return f'Node( Leaf {self.value} {self.right.__str__()} )'
        return f'Node( Leaf {self.value} Leaf )'
    

def left_rotate(root, x: Node):
    y: Node = x.right
    x.right = y.left
    if y.left:
        y.left.parent = x
    y.parent = x.parent
    if not x.parent:
        root = y
    elif x.parent.left == x:
        x.parent.left = y
    else:
        x.parent.right = y
    y.left = x
    x.parent = y
        

def insert(root, value: int):
    if not root:
        return Node(value, parent=root)
    
    if value < root.value:
        root.left = insert(root.left, value)
    
    if value > root.value:
        root.right = insert(root.right, value)

    return root

root = Node(10)

insert(root, 20)
left_rotate(root, root.right)

print(root)