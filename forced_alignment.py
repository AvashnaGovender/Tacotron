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

os.system(f'python scripts/prepare_txt_done_data_file.py {hp.data_path}/train.csv {hp.data_path}/utts.data')

# Check if Festival is installed

if not "festival" in os.listdir("tools"):
    print("Festival is not installed!!")
    print("Install festival using: bash tools/compile_festival.sh ")
    exit()


print("Preparing full-contextual labels without timestamps using Festival frontend ... ")

inp_txt = f'{hp.data_path}/utts.data'
lab_dir = f'{hp.data_path}/labels'


### generate a scheme file
os.system(f'python scripts/genScmFile.py \
        {inp_txt} \
        {lab_dir}/prompt-utt \
        {lab_dir}/train_sentences.scm \
        {lab_dir}/file_id_list.scp')


exit()

# Check wav files and txt files are equal

for book in hp.book_names:

    wav_path = os.path.join(hp.wav_path, book)
    txt_path = os.path.join(hp.txt_path, book)

    assert len(os.listdir(txt_path) ) == len(os.listdir(wav_path))



# Run state aligner

#./scripts/run_state_aligner.sh $wav_dir $inp_txt $lab_dir $global_config_file
# Check that txtdir is not empty

if len(os.listdir(hp.txt_path) ) == 0:
    print("Text Directory is empty - Please run utils/create_txt_files.py first")
    exit()

#Convert to utts.data format

os.system(f'python {hp.ROOT}/utils/prepare_txt_done_data_file.py {hp.txt_path} etc/txt.done.data ')

# Create symbolic links to wavs_dir
#os.system(f'ln -s {hp.wav_path} full_wav')
#os.system(f'mkdir wav')

# Downsample wavs to 16kHz

#for wav_file in os.listdir('full_wav'):
#    if '.wav' in wav_file:
#        os.system(f'sox full_wav/{wav_file} -r 16000 wav/{wav_file}')




os.system('./bin/do_build build_prompts')
os.system('./bin/do_build label')
os.system('./bin/do_build build_utts')
os.system(f'cp -r lab/*.lab {hp.data_path}/labels')


os.chdir(f'{hp.data_path}')
os.system(f'cat cmu_us_{hp.tts_model_id}/etc/txt.done.data | cut -d " " -f 2 > file_id_list.scp')
ls

print("Converting festival utts to labels...")

os.system(f'{hp.ROOT}/utils/festival_utt_to_lab/make_labels \
                        full-context-labels \
                        {hp.data_path}/cmu_us_{hp.tts_model_id}/festival/utts \
                        {hp.fest}/examples/dumpfeats \
                        {hp.ROOT}/utils/festival_utt_to_lab')


print("normalizing label files for merlin...")
os.system(f'python {hp.ROOT}/utils/normalize_lab_for_merlin.py \
                        full-context-labels/full \
                        label_phone_align \
                        phone_align \
                        file_id_list.scp')
