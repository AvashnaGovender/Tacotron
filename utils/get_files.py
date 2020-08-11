with open("trainset-transcript.csv") as f:
  all_content = f.readlines()

with open("selected_files_2booksduration.txt") as g:
  filenames = g.readline()


for line in all_content:
    filename = line.split("|")[0]
    if filename in filenames:
      print(line)
