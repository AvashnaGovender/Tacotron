from utils import hparams as hp
import os
import argparse
from utils.paths import Paths

#NB: Please run utils/create_txt_files.py to generate txt files needed for forced alignment

parser = argparse.ArgumentParser(description='Forced alignment for Tacotron')
parser.add_argument('--hp_file', metavar='FILE', default='hparams.py', help='The file to use for the hyperparameters')
args = parser.parse_args()

print(args.hp_file)
hp.configure(args.hp_file)  # Load hparams from file


#Setup paths
paths = Paths(hp.data_path, hp.voc_model_id, hp.tts_model_id)

# Check if train.csv file in data path

if not "train.csv" in os.listdir(hp.data_path):
    print(f'Please place train.csv file in the directory specificed in {hp.data_path} in hparams.py')
    exit()

# Create utts.data from metadata.csv file
print("Creating utts.data file ... ")

#os.system(f'python scripts/prepare_txt_done_data_file.py {hp.data_path}/train.csv {hp.data_path}/utts.data')

# Check if Festival is installed

if not "festival" in os.listdir("tools"):
    print("Festival is not installed!!")
    print("Install festival using: bash tools/compile_festival.sh ")
    exit()


print("Preparing full-contextual labels without timestamps using Festival frontend ... ")

inp_txt = f'{hp.data_path}/utts.data'
lab_dir = f'{hp.data_path}/labels'


### generate a scheme file
# os.system(f'python scripts/genScmFile.py \
#         {inp_txt} \
#         {lab_dir}/prompt-utt \
#         {lab_dir}/train_sentences.scm \
#         {lab_dir}/file_id_list.scp')


## create utts using FESTIVAL
print("Creating utterances --  NB: takes a while ... ")
#os.system(f'tools/festival/bin/festival -b {lab_dir}/train_sentences.scm')



print("Converting festival utts to labels...")

os.system(f'scripts/festival_utt_to_lab/make_labels \
                        {lab_dir}/prompt-lab \
                        {lab_dir}/prompt-utt \
                        tools/festival/examples/dumpfeats \
                        scripts/festival_utt_to_lab ')


print("Normalizing label files for merlin...")

os.system(f'python scripts/normalize_lab_for_merlin.py \
                            {lab_dir}/prompt-lab/full \
                            {lab_dir}/label_no_align \
                            phone_align \
                            {lab_dir}/file_id_scp 0 ')


if len(os.listdir(f'{lab_dir}/prompt-lab')) == 0:
    print("Something went wrong in label creation!")
else:
    print(f'Labels are ready in: {lab_dir}/prompt-lab !!"')

exit()
