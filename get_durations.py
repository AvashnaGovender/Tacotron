import numpy as np
from pathlib import Path
from scipy.spatial.distance import cdist

def plain_phone_label_to_monophones(labfile):
    labels = np.loadtxt(labfile, dtype=str, comments='#') ## default comments='#' breaks
    starts = labels[:,0].astype(int)
    ends = labels[:,1].astype(int)
    mono = labels[:,2]
    lengths = (ends - starts) / 10000 ## length in msec
    return (mono, lengths)

def merlin_state_label_to_monophones(labfile):
    labels = np.loadtxt(labfile, dtype=str, comments=None) ## default comments='#' breaks
    starts = labels[:,0].astype(int)[::5]
    ends = labels[:,1].astype(int)[4::5]
    fc = labels[:,2][::5]
    mono = [label.split('-')[1].split('+')[0] for label in fc]
    # return zip(starts, ends, mono)
    lengths = (ends - starts) / 10000 ## length in msec
    return (mono, lengths)

def resample_timings(lengths, from_rate=5.0, to_rate=12.5, total_duration=0):
    '''
    lengths: array of durations in msec. Each value is divisible by from_rate.
    Return converted sequence where values are divisible by to_rate.
    If total_duration, increase length of *last* item to match this total_duration.
    '''


    remainder = lengths % from_rate

    assert remainder.sum() == 0.0

    ## find closest valid end given new sample rate
    ends = np.cumsum(lengths)
    new_valid_positions = np.arange(0,ends[-1] + (from_rate*3),float(to_rate))
    distances = cdist(np.expand_dims(ends,-1), np.expand_dims(new_valid_positions, -1))
    in_new_rate = new_valid_positions[distances.argmin(axis=1)]
    if 0:
        print(zip(ends, in_new_rate))

    ## undo cumsum to get back from end points to durations:
    in_new_rate[1:] -= in_new_rate[:-1].copy()

    if total_duration:
        diff = total_duration - in_new_rate.sum()
        assert in_new_rate.sum() <= total_duration, (in_new_rate.sum(), total_duration)
        assert diff % to_rate == 0.0
        in_new_rate[-1] += diff

    return in_new_rate


def main_work():
   labfile = Path('/Users/avashnagovender/Development/merlin/egs/build_your_own_voice/s1/database/labels/label_state_align/CB-JE-01-104.lab')
   (mono, lengths) =   merlin_state_label_to_monophones(labfile)


   mel_file = labfile.stem
   mel_features = np.load(f'data/data/test/mel/{mel_file}.npy')
   audio_msec_length = mel_features.shape[1] * 12.5


   resampled_lengths = resample_timings(lengths, from_rate=5.0, to_rate=12.5, total_duration=audio_msec_length)

   resampled_lengths_in_frames = (resampled_lengths / 12.5).astype(int)
   print(mono, resampled_lengths_in_frames)

   #timings = match_up((mono, resampled_lengths_in_frames), transcript[labfile.stem]['phones'])


if __name__=="__main__":
    main_work()
