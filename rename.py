import os

def main():

  old_name = input("Old name: ")
  new_name = input("New name: ")

  with open("result.txt", "r") as f:
    file = f.read()

  file = file.replace(old_name, new_name)

  with open("result.txt", "w") as f:
    f.write(file)

if __name__ == "__main__":
    main()