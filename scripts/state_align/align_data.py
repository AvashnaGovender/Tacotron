import os, sys, argparse
import time
import random, glob
from sys import argv, stderr
from subprocess import check_call, Popen, CalledProcessError, PIPE
from mean_variance_norm import MeanVarianceNorm


def align(work_dir, lab_align_dir, model_dir, lab_dir):
    """
    Align using the models that have been trained with a different datatset
    """
    print('---aligning data')
    print(time.strftime("%c"))
    align_mlf = os.path.join(work_dir, 'mono_align.mlf')
    mono_lab_dir = os.path.join(work_dir, 'mono_no_align')
    cfg = os.path.join(work_dir, 'config', 'cfg')
    train_scp = os.path.join(work_dir, 'config', 'train.scp')
    phoneme_mlf = os.path.join(work_dir, 'config', 'mono_phone.mlf')
    model= os.path.join(model_dir, 'model', 'hmm_mix_32_iter_0') #bc
    phoneme_map = os.path.join(model_dir, 'phoneme_map.dict')
    phonemes = os.path.join(model_dir, 'mono_phone.list')

    check_call([HVite, '-a', '-f', '-m', '-y', 'lab', '-o', 'SM',
                '-i', align_mlf, '-L', mono_lab_dir,
                '-C', cfg, '-S', train_scp,
                '-H', os.path.join(model_dir, MACROS),
                '-H', os.path.join(model_dir, HMMDEFS),
                '-I', phoneme_mlf, '-t'] + PRUNING +
               ['-s', SFAC, phoneme_map, phonemes])

    _postprocess(align_mlf, lab_align_dir, lab_dir)

def _postprocess(mlf, lab_align_dir, lab_dir):

    if not os.path.exists(lab_align_dir):
        os.makedirs(lab_align_dir)

    state_num = STATE_NUM
    fid = open(mlf, 'r')
    line = fid.readline()
    while True:
        line = fid.readline()
        line = line.strip()
        if len(line) < 1:
            break
        line = line.replace('"', '')
        file_base = os.path.basename(line)
        flab = open(os.path.join(lab_dir, file_base), 'r')
        fw   = open(os.path.join(lab_align_dir, file_base), 'w')
        for full_lab in flab.readlines():
            full_lab = full_lab.strip()
            for i in range(state_num):
                line = fid.readline()
                line = line.strip()
                tmp_list = line.split()
                fw.write('{0} {1} {2}[{3}]\n'.format(tmp_list[0], tmp_list[1], full_lab, i+2))

        fw.close()
        flab.close()
        line = fid.readline()
        line = line.strip()
        if line != '.':
            print('The two files are not matched!\n')
            sys.exit(1)
    fid.close()

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Forced alignment')
    parser.add_argument('--lab_dir', metavar='FILE', required = True, help='The directory containing labels')
    parser.add_argument('--wav_dir', metavar='FILE', required = True, help='The directory containing wavs')

    args = parser.parse_args()


    work_dir = args.lab_dir

    wav_dir = args.wav_dir

    lab_dir = os.path.join(work_dir, 'label_no_align')
    lab_align_dir = os.path.join(work_dir, 'label_state_align')

    file_id_list_name = os.path.join(work_dir, 'file_id_list.scp')

    align(work_dir, lab_align_dir, model_dir, lab_dir)
