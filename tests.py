from functions.run_python import run_python_file

def main():
    print("------------")
    print(run_python_file("calculator", "main.py"))
    print("------------")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("------------")
    print(run_python_file("calculator", "tests.py"))
    print("------------")
    print(run_python_file("calculator", "../main.py"))
    print("------------")
    print(run_python_file("calculator", "nonexistent.py"))


if __name__ == "__main__":
    main()