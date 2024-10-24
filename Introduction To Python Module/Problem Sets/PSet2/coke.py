total_amount = 0
while total_amount < 50:
    coin = int(input("Insert a coin: "))
    if coin == 25 or coin == 10 or coin == 5:
        total_amount += coin

change = total_amount - 50
print(change, "cents")
