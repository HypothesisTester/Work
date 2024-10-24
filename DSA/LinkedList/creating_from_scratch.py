class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None
        
    # Need to make sure that our next pointers point to another ListNode, and not null
    ListNode1.next = ListNode2

    # Next, setting the next pointer for ListNode2 and ListNode3.
    ListNode2.next = ListNode3
    ListNode3.next = null