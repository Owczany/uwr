class Node:
    """Węzeł drzewa binarnego."""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __repr__(self):
        return f"TreeNode({self.value})"
    
class Tree:
    def __init__(self):
        self.root = None
        
    def insert(self, value):
        if self.root:
            self._insert_recursive(self.root, value)    
        else:
            self.root = Node(value)
            
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Węzeł bez dzieci
            if node.left is None and node.right is None:
                return None
            # Węzeł z jednym dzieckiem
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Węzeł z dwoma dziećmi
            else:
                successor = self._find_min(node.right)  # Znajdujemy następnik
                node.value = successor.value  # Podmieniamy wartość
                node.right = self._delete_recursive(node.right, successor.value)  # Usuwamy następnik

        return node

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node
            
    def _height_recursive(self, node):
        if node is None:
            return 0
            
        return max(self._height_recursive(node.left), self._height_recursive(node.right)) + 1
                  
    def height(self):
        return self._height_recursive(self.root)
        
    def max_distance_between_nodes(self):
        if self.root is None:
            return 0
        
        return self._height_recursive(self.root.left) + self._height_recursive(self.root.right) + 1
            
    # Funkcja pomocnicza do wstawiania elementu
    def _insert_recursive(self, node, value):
        # Sprawdzanie czy wartość jest mniejsza od aktualnej wartości node'a
        if value < node.value:
            if node.left:
                self._insert_recursive(node.left, value)
            else:
                node.left = Node(value)
        else:
            if node.right:
                self._insert_recursive(node.right, value)
            else:
                node.right = Node(value)


    def find_successor(self, value):
        successor = None
        node = self.root

        while node:
            if value < node.value:
                successor = node  # Możliwy następnik
                node = node.left
            else:
                node = node.right

        return successor.value if successor else None
            
            
                
    def number_of_nodes(self):
        def count_nodes(node):
            if node is None:
                return 0
            
            return count_nodes(node.left) + count_nodes(node.right) + 1
        
        return count_nodes(self.root)
    
    
    # Funkcja zwracająca wartość drzewa w porządku ()
    def in_order_traversal(self):
        if self.root is None:
            print('Tree is empty!')
            return None
        
        result = []
        def in_order_traversal_helper(node):
            if node.left:
                in_order_traversal_helper(node.left)
                
            result.append(str(node.value))
            
            if node.right:
                in_order_traversal_helper(node.right)
                
            
        in_order_traversal_helper(self.root)
        output = ' '.join(result)
        print(output)
        return output
    
    
                
                
''' -------------------------------------------------------------------------------------------------- '''

def main():
    tree = Tree()
    tree.insert(5)
    tree.insert(10)
    tree.insert(2)
    tree.insert(1)
    tree.insert(3)

    print(tree.number_of_nodes())
    tree.in_order_traversal()
    print(tree.height())
    print(tree.max_distance_between_nodes())
    print(tree.find_successor(6))
    tree.delete(10)
    tree.in_order_traversal()
    
''' -------------------------------------------------------------------------------------------------- '''

# Odpala program
if __name__ == "__main__":
    main()
            