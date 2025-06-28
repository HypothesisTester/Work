import sys

def main() -> None:
    it = sys.stdin.buffer.readline
    t = int(it())             # number of test cases
    out = []

    for _ in range(t):
        d = int(it())
        if d % 9:             # impossible
            out.append("NONE")
        else:
            y = d // 9        # smaller number (may be 0)
            x = y * 10        # larger number
            out.append(f"{x} {y}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()