def main():
    file_name = input("Enter file name: ")  # Get file name from user
    file_name_lower = file_name.lower()  # Convert to lowercase
    media_type = get_media_type(file_name_lower)  # Determine media type
    print("Media type:", media_type)


def get_media_type(file_name):
    # Identify media type based on file extension
    if file_name.endswith(".gif"):
        return "image/gif"
    elif file_name.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    elif file_name.endswith(".png"):
        return "image/png"
    elif file_name.endswith(".pdf"):
        return "application/pdf"
    elif file_name.endswith(".txt"):
        return "text/plain"
    elif file_name.endswith(".zip"):
        return "application/zip"
    else:
        return "application/octet-stream"


main()
