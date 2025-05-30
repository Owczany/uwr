# Tworzenie funkcji dla drzew BST - Binary Search Tree


class Node():
    def __init__(self, value: int, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

    def inorder(self, arr: list = []):
        if self.left:
            self.left.inorder(arr)
        arr.append(str(self.value))
        if self.right:
            self.right.inorder(arr)
        return arr
    
    def min(self):
        if not self.left:
            return self.value
        
        return self.left.min()

    def max(self):
        if not self.right:
            return self.value
        
        return self.right.max()
    
    def successor():
        pass
    
    def insert(self, val: int):
        if val <= self.value:
            if self.left:
                return self.left.insert(val)
            self.left = Node(val)

        else:
            if self.right:
                return self.right.insert(val)
            self.right = Node(val)

    def find(self, value: int):
        if self.value == value:
            return self
        elif value < self.value and self.left:
            return self.left.find(value)
        elif value > self.value and self.right:
            return self.right.find(value)
        return None

    def __str__(self):
        return ' '.join(self.inorder())
    

root = Node(10, Node(5), Node(15))

root.insert(12)
root.insert(3)
print(root)
print(root.min())
print(root.max())




        