import os


def get_files(path, books, extension='.csv'):
    filenames = []
    filepath = os.path.join(path,"train.csv")
    with open(filepath, "r") as f:
        content = f.readlines()

    content  = [x.strip() for x in content ]

    if len(books) != 0:
        for x in content:
            name  = x.split("|")[0]
            book = name.split("-")
            bookname = book[0]+"-"+book[1]

            if bookname in books:
                name = os.path.join(path, bookname, name)
            filenames += [name]
    else:
        for x in content:
            name  = x.split("|")[0]
            name = os.path.join(path,name)
            filenames += [name]



    return filenames
