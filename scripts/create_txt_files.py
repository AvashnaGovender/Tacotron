import os
import argparse
import codecs

# Helper script to create text files for forced alignment from
# the metadata.csv transcription file

parser = argparse.ArgumentParser(description='Create txt files')
parser.add_argument('--transcript', metavar='FILE', required = True, help='The file containing text transcripts')
parser.add_argument('--path', metavar='FILE', required = True, help='The file containing text transcripts')

args = parser.parse_args()


print(args.transcript)
print(args.path)

transcript = args.transcript
path = args.path

with open(transcript, 'r') as f:
    content = f.readlines()

#
for line in content:
    txt = line.split('|')[2]
    filename = line.split('|')[0]

    file1 = open(f'{path}/{filename}.txt', 'w')
    file1.write(txt)
    file1.close()

# utts.data format

# for line in content:
#     txt = line.split('\"')[1]
#     filename = line.split(' ')[1]
#
#     with codecs.open(f'{path}/{filename}.txt', 'w', "utf-8") as file1:
#         file1.write(txt)
#     file1.close()
