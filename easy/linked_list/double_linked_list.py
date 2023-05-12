class Node:
    def __init__(self, data):
        self.data=data
        self.next=None
        self.prev=None

    def __repr__(self):
        return repr(self.data)

class DoubleLinkedList:
    def __init__(self, nodes=None):
        self.head=None
        self.butt=None
        if nodes is not None and nodes:
            node=Node(data=nodes.pop(0))
            self.head=node
            prev_node=None
            for item in nodes:
                node.next=Node(item)
                node.prev=prev_node
                prev_node=node
                node=node.next
            self.butt=prev_node


    def __repr__(self):
        node=self.head
        nodes=[]
        r_node=self.butt
        r_nodes=[]

        while node is not None:
            nodes.append(node.data)
            node=node.next
        nodes.append("None")

        while r_node is not None:
            r_nodes.append(r_node.data)
            r_node=r_node.prev
        r_nodes.append("None")
        return " <--> ".join(map(str, nodes)) + "\n ------ \n" +  " <--> ".join(map(str, r_nodes))

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node=node.next

    def __reversed__(self):
        node = self.head
        while node.next is not None:
            node=node.next

        while node is not None:
            yield node
            node=node.prev

    def insert_first(self, node):
        node.next=self.head
        self.head=node

    def insert_last(self, node):
        if self.head is None: 
            self.head=node
            return

        for current_node in self:
            pass
        current_node.next=node
        self.butt=node

    def insert_after(self, target_node_data, new_node):
        """inserts a node after the first instance"""
        if self.head is None:
            raise Exception("List is empty...")

        for node in self:
            if node.data == target_node_data:
                new_node.next=node.next
                node.next=new_node
                return
        raise Exception("Desired node ($s) not found..." % target_node_data)

    def insert_before(self, target_node_data, new_node):
        """inserts a node before the first instance"""
        if self.head is None:
            raise Exception("List is empty...")

        if self.head.data == target_node_data:
            return self.insert_first(new_node)

        prev_node=self.head    
        for node in self:
            if node.data == target_node_data:
                new_node.next=node
                prev_node.next=new_node
                return
            prev_node=node
        raise Exception("Desired node ($s) not found..." % target_node_data)

    def remove_first(self):
        if self.head is None:
            raise Exception("Can't remove a node because the list is empty")

        self.head=self.head.next

    def remove_last(self):
        if self.head is None:
            raise Exception("Can't remove a node because the list is empty")


    def remove_node(self, target_node_data):
        if self.head is None:
            raise Exception("Can't remove a node because the list is empty")
        if self.head.data == target_node_data:
            return self.remove_first()

        prev_node=self.head    
        for node in self:
            if node.data == target_node_data:
                prev_node.next=node.next
                return
            prev_node=node
        raise Exception("Desired node ($s) not found..." % target_node_data)


l=DoubleLinkedList(nodes=['a', 33, False])
l.insert_last(Node('jjj'))
l.insert_first(Node(9))
l.insert_after(33, Node('after33'))
l.insert_before(33, Node('b433'))
l.insert_after(9, Node('after9'))
l.insert_before(9, Node('b49'))
l.insert_after('jjj', Node('afterjjj'))
l.insert_before('jjj', Node('b4jjj'))

l.remove_first()

for i in reversed(l):
    print(i)




