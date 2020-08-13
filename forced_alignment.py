from utils import hparams as hp
import os
import argparse
from utils.paths import Paths

#NB: Before running script makesure you have FESTVOXDIR, ESTDIR and FESTIVAL paths set

parser = argparse.ArgumentParser(description='Forced alignment for Tacotron')
parser.add_argument('--hp_file', metavar='FILE', default='hparams.py', help='The file to use for the hyperparameters')
args = parser.parse_args()

print(args.hp_file)
hp.configure(args.hp_file)  # Load hparams from file


# Check that festival, speech_tools and festvox are setup
if not os.path.isdir(hp.speech_tools):
    print("Please install speech tools ")
    exit()


if not os.path.isdir(hp.fest):
    print("Please install Festival ")
    exit()

if not os.path.isdir(hp.festvox):
    print("Please install Festvox")
    exit()


print(hp.festvox)
print(hp.fest)
print(hp.speech_tools)


print("All tools are fine!")

#Setup paths
paths = Paths(hp.data_path, hp.voc_model_id, hp.tts_model_id)

# Setup clustergen

os.chdir(f'{hp.data_path}/cmu_us_{hp.tts_model_id}')
os.system(f'{hp.festvox}/src/clustergen/setup_cg cmu us {hp.tts_model_id}')

# Check that txtdir is not empty

if len(os.listdir(hp.txt_path) ) == 0:
    print("Text Directory is empty - Please run utils/create_txt_files.py first")
    exit()

#Convert to utts.data format

os.system(f'python {hp.ROOT}/utils/prepare_txt_done_data_file.py {hp.txt_path} etc/txt.done.data ')

# Create symbolic links to wavs_dir
os.system(f'ln -s {hp.wav_path} wav')

os.system('./bin/do_build build_prompts')
os.system('./bin/do_build label')
os.system('./bin/do_build build_utts')
os.system(f'cp -r lab/*.lab {hp.data_path}/labels')


os.chdir(f'{hp.data_path}')
os.system(f'cat cmu_us_{hp.tts_model_id}/etc/txt.done.data | cut -d " " -f 2 > file_id_list.scp')
