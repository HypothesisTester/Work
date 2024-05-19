class BrowserHistory:

    def __init__(self, homepage: str):
        
    def visit(self,url: str) -> None:
        
    
    def back(self, steps: int) -> str:
        
    
    def forward(self, steps: int) -> str:
        
    
    # Your BrowserHistory object will be instantiated and called as such:
# obj = BrowserHistory(homepage)
# obj.visit(url)
# param_2 = obj.back(steps)
# param_3 = obj.forward(steps)

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
        Self.prev = None
        

class BrowserHistory:
    
    def __init__(self, homepage: str):
        self.root = ListNode(homepage)
        
    def visit(self, url: str) -> None:
        node = ListNode(url)