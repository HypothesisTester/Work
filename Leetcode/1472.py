class ListNode:
    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next
        
class BrowserHistory:

    def __init__(self, homepage: str):
        self.cur = ListNode(homepage)
        

    def visit(self, url: str) -> None:
        self.cur.next = ListNode(url, self.cur)
        

    def back(self, steps: int) -> str:
        

    def forward(self, steps: int) -> str:
        


# Your BrowserHistory object will be instantiated and called as such:
# obj = BrowserHistory(homepage)
# obj.visit(url)
# param_2 = obj.back(steps)
# param_3 = obj.forward(steps)