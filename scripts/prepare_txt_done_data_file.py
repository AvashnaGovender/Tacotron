import os
import sys
import numpy as np
import codecs
if __name__ == "__main__":

    if len(sys.argv)!=3:
        print('Usage: python src/prepare_txt_done_data_file.py <meta_file> <utts.data>\n')
        sys.exit(0)

    meta_file  = sys.argv[1]
    out_file = sys.argv[2]

    out_f = open(out_file,'w')

    with open(meta_file, "r") as f:
        content = f.readlines()


    for text in content:
        data = text.split("|")
        t = data[2]
        file_id = data[0]

        out_f.write("( "+file_id+" \" "+t+" \")\n")

    out_f.close()
