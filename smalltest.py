class A:
  def __init__(self) -> None:
    self.s = 0
  def changes(self,a):
    self.s = a
  def print(self):
    print(self.s)
    
def test(a):
  a.changes(1)

def main():
  a = A()
  a.print()
  test(a)
  a.print()
  
main()