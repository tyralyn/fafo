""" Get the kth to last item int he linked list.

* There is no 0th to last item. 
* The 1st to last item is the last item (index=-1).
* The 2nd to last item is the item at index (index=-2).

"""
from linked_list import *

def return_kth_to_last(ll, k):
    # get the length of the linked list
    list_length = len(list(iter(ll)))

    if k <= 0:
        raise Exception("You asked for the {}th item, but k has to be greater than 0.".format(k))

    if list_length < k:
        raise Exception("You asked for the {} to last item, but the list only has {} item.".format(str(k), str(list_length)) )

    hold_node = ll.head
    for i in range(list_length - k):
        hold_node=hold_node.next
    return hold_node





l=LinkedList(nodes=['a', 33, False, 'bagpipe', -99, 233.55])