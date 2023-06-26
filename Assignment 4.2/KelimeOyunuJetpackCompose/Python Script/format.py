import os


# read all the text files and format them
def formatfiles():
    # read all the text files
    print("Formatting files...")
    for file in os.listdir("text"):
        # open the file
        with open("text/" + file, "r") as f:
            new_text = ""
            #     read the file line by line
            text = f.readlines()
            for line in text:
                if len(line) <= 3:
                    continue
                if line.__contains__(" "):
                    continue
                new_text += line
        with open("textfiltered/" + file, "w") as f:
            f.write(new_text)


formatfiles()
