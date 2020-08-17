'''
Author: JavanTang
Data: Do not edit
LastEditors: JavanTang
LastEditTime: 2020-08-17 11:44:35
Description: 
'''
from py2aliyungdb import Graph,Node,Relationship

g = Graph('bolt://127.0.0.1:7687',auth=('neo4j', '1234'))
g.connect()

_ = {
    'name':'c1',
    'id':1
}

n1 = Node('d', **_)
n2 = Node('d', name='c2', id=2)
n3 = Node('d', name='c3', id=3)
n4 = Node('d', name='c4', id=4)

g.create(n1)
g.create(n2)
g.create(n3)
g.create(n4)

r_1 = Relationship(n1, n2, 'r_1', is_exist_node=True)
r_2 = Relationship(n2, n3, 'r_2', is_exist_node=True)
r_3 = Relationship(n3, n4, 'r_3', is_exist_node=True)
r_4 = Relationship(n4, n1, 'r_4', is_exist_node=True)

g.create(r_1)
g.create(r_2)
g.create(r_3)
g.create(r_4)


