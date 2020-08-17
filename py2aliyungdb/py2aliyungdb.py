'''
Author: JavanTang
Data: 2020-08-13 10:11:39
LastEditors: JavanTang
LastEditTime: 2020-08-17 10:57:09
Description: 阿里云无法用py2neo直接操作,于是写一个基于neo4j包类似py2neo的包
'''
import json
from neo4j import GraphDatabase


def key2neo(d: dict):
    """The dictionary types into secondary string types available

    Args:
        d (dict): {"name":"node1"}

    Returns:
        str: {name:'node1'}
    """
    res = []
    for k, v in d.items():
        if isinstance(v, str):
            match = "{}: '{}'".format(k, v)
        else:
            match = "{}: {}".format(k, v)
        res.append(match)
    return "{" + ','.join(res) + "}"


class Entity(object):

    def __init__(self):
        self.is_create = False
        self.command = None
        self.__updata_command()

    def __updata_command(self):
        return ImportError

    def create(self):
        return ImportError


class Node(Entity):
    def __init__(self, label, **properties):
        """CREATE (n1:{label} {properties}) 

        Args:
            label (str): The category of the entity
        """
        self.label = label
        self.properties = properties
        self.__updata_command()
        super(Entity, self).__init__()

    def __updata_command(self):
        self.command = "MERGE(n1:{} {}) return n1".format(
            self.label, key2neo(self.properties))


class Relationship(Entity):
    def __init__(self, node1: Node, node2: Node, relation: str, is_exist_node: bool, two_way=False):
        """CREATE (n1)-[:{relation}]->(h1)
        create(:P {name:'黑'})-[:spouse]->(:P {name:'白'})

        Args:
            node1 (Node): [description]
            node2 (Node): [description]
            is_exist_node (bool): If there is a node
            relation (str): [description]
            two_way (bool): 
        """
        self.node1 = node1
        self.node2 = node2
        self.is_exist_node = is_exist_node
        self.relation = relation
        self.two_way = two_way
        self.__updata_command()
        super(Entity, self).__init__()

    def create(self):
        self.is_create = True
        self.node1.is_create = True
        self.node1.is_create = True

    def __updata_command(self):
        if self.two_way:
            self.create_command = "MERGE(n1:{} {})-[:{}]->(n2:{} {})\n".format(self.node1.label, key2neo(self.node1.properties), self.relation,
                                                                               self.node2.label, key2neo(self.node2.properties))
            self.create_command += "MERGE(n3:{} {})-[:{}]->(n4:{} {})".format(self.node2.label, key2neo(self.node2.properties), self.relation,
                                                                              self.node1.label, key2neo(self.node1.properties))
            # self.create_command += "return n1,n2,n3,n4"
        else:
            self.create_command = "MERGE(n1:{} {})-[:{}]->(n2:{} {})\n".format(self.node1.label, key2neo(self.node1.properties), self.relation,
                                                                               self.node2.label, key2neo(self.node2.properties))
            # self.create_command += "return n1,n2"

        if self.two_way:
            self.merge_command = """
                                MATCH (n1:{} {}),(n2:{} {})
                                MERGE  
                                    (n1)-[r:{}]->(n2)
                                    (n2)-[r:{}]->(n1)
                                """.format(self.node1.label, key2neo(self.node1.properties), 
                                           self.node2.label, key2neo(self.node2.properties), 
                                           self.relation, self.relation)
        else:
            self.merge_command = """
                                MATCH (n1:{} {}),(n2:{} {})
                                MERGE  
                                    (n1)-[r:{}]->(n2)
                                """.format(self.node1.label, key2neo(self.node1.properties), 
                                           self.node2.label, key2neo(self.node2.properties), 
                                           self.relation)
        if self.is_exist_node:
            self.command = self.merge_command
        else:
            self.command = self.create_command


class Graph(object):
    def __init__(self, url: str, auth: tuple):
        """          
        Args:             
            url (str): The pre_url can be bolt:// or neo4j://,                            
                        e.g bolt://127.0.0.1:7687 or neo4j://127.0.0.1:7687             
            auth (tuple): Your account password, e.g ('neo4j', '1234') 
        """
        self.driver = GraphDatabase.driver(url,
                                           auth=auth,
                                           encrypted=False)
        self.session = None

    def connect(self):
        if self.session is None or self.session._closed == True:
            self.session = self.driver.session()

    def close(self):
        if self.session is None:
            pass
        else:
            self.session.close()

    def matching(self, query):
        self.connect()
        result = self.session.run(query)
        values = []
        for ix, record in enumerate(result):
            values.append(record.values())
        # <neo4j.work.summary.ResultSummary object at 0x7fdaaaacac18>
        # 这里的ResultSummary还没有怎么理解
        info = result.consume()
        print(values)
        print(info)

    def create(self, x: Entity):
        """[summary]

        Args:
            x ([type]): [description]
        """
        self.connect()
        
        result = self.session.run(x.command)
        values = []
        for ix, record in enumerate(result):
            values.append(record.values())
        info = result.consume()
        print(x.command)
        print(values)
        print(info)


if __name__ == "__main__":
    g = Graph('bolt://127.0.0.1:7687', auth=('neo4j', '1234'))
    # result = g.matching('match(n1:node {name:"node1"})-[:设备]->(n2) return n1,n2')
    node_1 = Node('nd', name='node_1')
    node_2 = Node('nd', name='node_2')
    r_1 = Relationship(node_1, node_2, '设备')
    g.create(r_1)
    # g.create(node_1)
