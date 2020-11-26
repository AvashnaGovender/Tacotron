### Recipe to create Pre-alignment guides for training

**Step 1 - Install tools**

> cd tools

> bash compile_festival.sh

If you dont already have an account with HTS, you need to create one in order to download HTK. 
Get an account here: [htk](http://htk.eng.cam.ac.uk/register.shtml) as you will need a username and password for the next step

> bash compile_htk.sh $username $password

To test HTK and Festival is installed and working, the following should run without error:

> HCopy

> festival

**Step 2 - Get data**

> mkdir data

> cd data

> wget **link to data**

> cp -f train.csv {data_path}


**Step 3 - Edit hparams.py**

    wav_path = 'data/wavs_train/'
    data_path = 'data/CB_JE'
    book_names = ['CB-JE']
    voc_model_id = 'blizzard_vocoder'
    tts_model_id = 'blizzard_baseline_JE'
    metadata = "train.csv"

**Step 4 - Extract features**

> python preprocess --hp_file hp_JE.py

**Step 5a - Run forced alignment**

> python forced_alignment.py --hp_file hp_JE.py

This will output all the necessary files for forced alignment in {data_path}/labels

**Step 5b - Run alignment on different model (optional)**

Since we only using 1 book in this recipe, it will be better to train the aligner with all the data. In this case, you need to run Step 5a with all the data and then run:

> python scripts/align_data.py --lab_dir {labels folder of JE book} --model_dir {labels folder of all books}

The output label files will be in {data_path}/labels/label_state_align

**Step 6 - Get durations and create guides**

> python get_durations.py --hp_file hp_JE.py

The output guides will be saved in {hp.data_path}/attention_guides

**Step 7 - Train PAG**

> python train_pag.py --hp_file hp_JE.py



