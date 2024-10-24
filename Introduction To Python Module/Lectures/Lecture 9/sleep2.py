def main():
    n = int(input("What's n? "))
    for s in sheep(n):
        print(s)

def sheep(n):
    for i in range(n):
        # yield is basically return 1 value at a time, returns value called an iterator
        yield "🐑" * i

if __name__ == "__main__":
    main()