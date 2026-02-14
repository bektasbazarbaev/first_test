class Account():
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
    def deposit(self):
        pass
    def withdraw(self, w_amount):
        if self.balance >= w_amount:
            print(self.balance - w_amount)
        else:
            print("Insufficient Funds")

data = list(map(int, input().split()))

p1 = Account("Ryan Gosling", data[0])
p1.withdraw(data[1])