import os
import argparse
from utils import hparams as hp
from utils.paths import Paths
import pickle

parser = argparse.ArgumentParser(description='Check preprocess was performed correctly')
parser.add_argument('--hp_file', metavar='FILE', default='hparams.py', help='The file to use for the hyperparameters')
args = parser.parse_args()

print(args.hp_file)
hp.configure(args.hp_file)  # Load hparams from file

paths = Paths(hp.data_path, hp.voc_model_id, hp.tts_model_id)


text_inputs = f'{hp.data_path}/text_dict.pkl'
mel_inputs = f'{hp.data_path}/dataset.pkl'

with open(text_inputs, 'rb') as f:
  i_content = pickle.load(f)

print("Text input dim:", len(i_content))

with open(mel_inputs, 'rb') as f:
  m_content = pickle.load(f)


print("Mel input dim:", len(m_content))

dataset_ids_1 = [x for x in i_content]
dataset_ids_2 = [x for x in m_content]

print(dataset_ids_1[:3])
print(dataset_ids_2[:3])
