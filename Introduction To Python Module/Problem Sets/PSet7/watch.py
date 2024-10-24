import re
import sys


def main():
    print(parse(input("HTML: ")))


def parse(s):
    # Regular expression pattern for iframe src attribute with YouTube URL
    pattern = r"https?://(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)"

    # Find the first URL that matches the pattern
    match = re.search(pattern, s)

    if match:
        # If a match is found, return the shorter, shareable youtu.be URL
        video_id = match.group(1)
        return f"https:youtu.be/{video_id}"

    # If no match is found, return None
    return None


if __name__ == "__main__":
    main()
