from typing import List, Optional, Tuple
import json


class TreeNode:
    def __init__(self, value=None):
        self.isWord = False
        self.currentValue = value
        self.children: List[TreeNode] = []
        self.childrenValues = set()
        # the index of word in storage, which will be updated if current node is the end of word
        self.index = -1
    
    def addChild(self, value) -> "TreeNode":
        if value not in self.childrenValues:
            self.childrenValues.add(value)
            newNode = TreeNode(value)
            self.children.append(newNode)
            return newNode
        else:
            return self.next(value)
    
    def markWord(self, index):
        self.isWord = True
        self.index = index
    
    def next(self, value)->Optional["TreeNode"]:
        for child in self.children:
            if child.currentValue == value:
                return child
        return None


class Trie:

    def __init__(self):
        self.root = TreeNode()

    def insert(self, word: str, word_idx: int) -> None:
        current = self.root
        for i in word:
            nextNode = current.addChild(i)
            current = nextNode
        current.markWord(word_idx)

    def search(self, word: str) -> (bool, int):
        current = self.root
        for i in word:
            nextNode = current.next(i)
            if not nextNode:
                return False, -1
            current = nextNode
        return current.isWord, current.index

    def startsWith(self, prefix: str) -> bool:
        current = self.root
        for i in prefix:
            nextNode = current.next(i)
            if not nextNode:
                return False
            current = nextNode
        return True
    
    def searchWithPrefix(self, prefix: str) -> List[Tuple[str, int]]:
        current = self.root
        for i in prefix:
            nextNode = current.next(i)
            if not nextNode:
                return []
            current = nextNode
        res = []
        self.dfs(current, prefix, res)
        return res

    def dfs(self, node: TreeNode, current_str: str, postfix: List[Tuple[str, int]]) -> None:
        current_str += node.currentValue
        if node.isWord:
            postfix.append((current_str, node.index))
            return
        else:
            for child in node.children:
                self.dfs(child, current_str, postfix)
            return
    
    # TODO: find out a good way to store and load trie tree
    def save_to_file_bfs(self, file_path: str):
        return
    
    def load_from_file_bfs(self, file_path: str):
        return