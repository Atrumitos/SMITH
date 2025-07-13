from functions.get_file_content import get_file_content

def main():
    print("------------")
    print(get_file_content("calculator", "main.py"))
    print("------------")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("------------")
    print(get_file_content("calculator", "/bin/cat"))
    print("------------")


if __name__ == "__main__":
    main()