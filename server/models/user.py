from py2neo import Node, Relationship
from .node import Node

class User(Node):
    def __init__(self, name):
        self.name = name
        self.username=""
        self.password=""
        self.myDict={"username":self.username,"password":self.password}
        self.node=Node("User", name=self.name)
        self.node.update(self.myDict)

    def setUsername(self,userName):
        self.node.update(self.myDict)

    def setPassword(self,password):
        self.password=password
