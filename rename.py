import os

def main():

  old_name = input("Old name: ")
  new_name = input("New name: ")
  file_name = input("File name where the result is stored (most likely result.txt): ")

  with open(file_name, "r") as f:
    file = f.read()

  file = file.replace(old_name, new_name)

  with open(file_name, "w") as f:
    f.write(file)

  print("Done!")

if __name__ == "__main__":
    main()