import re
import sys


def main():
    inp: str = input("IPv4 Address: ").strip()
    print(validate(inp))


def validate(ip: str):
    try:
        split_ip: list[str] = ip.split(".")  # Split input string

        if len(split_ip) != 4:  # Validate segment count
            return False

        for s in split_ip:  # Validate each segment
            if not s.isnumeric() or int(s) < 0 or int(s) > 255:
                return False

    except ValueError:  # Handle conversion errors
        return False

    return True  # If all checks pass, IP is valid


if __name__ == "__main__":
    main()
