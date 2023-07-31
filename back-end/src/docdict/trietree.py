from typing import List
class TreeNode:
    def __init__(self, value=None):
        self.isWord = False
        self.currentValue = value
        self.children: List[TreeNode] = []
        self.childrenValues = set()
    
    def addChild(self, value) -> TreeNode:
        if value not in self.childrenValues:
            self.childrenValues.add(value)
            newNode = TreeNode(value)
            self.children.append(newNode)
            return newNode
        else:
            return self.next(value)
    
    def markWord(self):
        self.isWord = True
    
    def next(self, value)->Optional[TreeNode]:
        for child in self.children:
            if child.currentValue == value:
                return child
        return None


class Trie:

    def __init__(self):
        self.root = TreeNode()

    def insert(self, word: str) -> None:
        current = self.root
        for i in word:
            nextNode = current.addChild(i)
            current = nextNode
        current.markWord()

    def search(self, word: str) -> bool:
        current = self.root
        for i in word:
            nextNode = current.next(i)
            if not nextNode:
                return False
            current = nextNode
        return current.isWord

    def startsWith(self, prefix: str) -> bool:
        current = self.root
        for i in prefix:
            nextNode = current.next(i)
            if not nextNode:
                return False
            current = nextNode
        return True