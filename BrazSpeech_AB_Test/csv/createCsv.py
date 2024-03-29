import pandas
import random
import os

my_path = os.path.abspath(os.path.dirname(__file__))

random.seed(1337)

NUMBER_OF_ACCENTS = 2

# OBS: THE VALUES FOR THE ARTICLE WILL BE 36, 12, 48
SYNTH_AMOUNT_XAB_PER_ACCENT = 36
SYNTH_AMOUNT_MOS_PER_ACCENT = 12
SYNTH_AMOUNT_TOTAL_PER_ACCENT = 48

# OBS: THE VALUES FOR THE ARTICLE WILL BE 18, 12, 30
NATURAL_AMOUNT_XAB_PER_ACCENT = 18
NATURAL_AMOUNT_MOS_PER_ACCENT = 12
NATURAL_AMOUNT_TOTAL_PER_ACCENT = 30


def create_csv(dataframe: pandas.DataFrame, path: str):
    """Creates a csv file with the given dataframe

    Args:
        dataframe (pandas.DataFrame): Dataframe to be written to the csv file
        path (str): Path to the csv file. Must include the file name and extension.
    """
    dataframe.sort_values(by=['email'], inplace=True)

    dataframe.to_csv(path, index=False)
    print("csv created from dataframe")


def pop_to_another_list(audio_files: list[str], new_list: list[str]):
    """Appends the given audio files to the new list, with the given accent.

    Args:
        audio_files (list[str]): List of audio files to be appended to the new list.
        accent (str): State acronym (lowercase) of the accent of the audio files.
        new_list (list[str]): List to which the audio files will be appended.
    """
    for i in range(len(audio_files)):
        new_list.append(audio_files.pop(0))


def add_to_mos_list(emails: list[str], lenght: int, audio_files: list[str], natural: str, row_list: list[str]):
    """Adds the given emails and audio files to the row list, that will be used to create the dataframe for the MOS test

    Args:
        emails (list[str]): List of emails to be added to the row list. Please verify if the accent is condizent with the audio files.
        lenght (int): Lenght of the test that is to be given to each student. Total row list size will be lenght * len(emails)
        audio_files (list[str]): List of audio files to be added to the row list. Please verify if the accent is condizent with the emails.
        natura (str): 'n' if the audio files are natural, 's' if the audio files are synthetic.
        row_list (list[str]): List of rows to be added to the dataframe
    """
    for i in range(lenght):
        if len(audio_files) == 0 or i >= SYNTH_AMOUNT_MOS_PER_ACCENT * 2:
            break
        for email in emails:
            row_list.append([email, audio_files[0], natural, ''])
        audio_files.pop(0)


def add_to_xab_x_natural_two_synth(emails: list[str], lenght: int, audio_files_natural: list[str], audio_files_correct: list[str], audio_files_wrong: list[str], accent_right: str, row_list: list[str]):
    """Adds the given emails and audio files to the row list, that will be used to create the dataframe for the XAB test,
    where the X audio is natural and both a and b are synthetic.

    Args:
        emails (list[str]): List of emails to be added to the row list. Please verify if the accent is condizent with the audio files and accent.
        lenght (int): Lenght of the test that is to be given to each student. Total row list size will be lenght * len(emails).
        audio_files_natural (list[str]): List of natural audio files. Please verify if the accent is condizent with the emails.
        audio_files_correct (list[str]): List of audio files with the right accent. Please verify if the accent is condizent with the emails.
        audio_files_wrong (list[str]): List of audio files with the wrong accent.
        accent_right (str): State acronym (lowercase) of the right accent.
        row_list (list[str]): List of rows to be added to the dataframe.
    """

    for i in range(lenght):
        if len(audio_files_natural) == 0 or len(audio_files_correct) == 0 or len(audio_files_wrong) == 0 or i >= SYNTH_AMOUNT_XAB_PER_ACCENT:
            break
        rng = random.randint(0, 1)
        for email in emails:
            if rng == 0:
                row_list.append([email, audio_files_natural[0], audio_files_correct[0], audio_files_wrong[0][0],
                                  accent_right, accent_right, audio_files_wrong[0][1], 's', ''])
            else:
                row_list.append([email, audio_files_natural[0], audio_files_wrong[0][0], audio_files_correct[0],
                                  accent_right, audio_files_wrong[0][1], accent_right, 's', ''])
                
        audio_files_natural.pop(0)
        audio_files_correct.pop(0)
        audio_files_wrong.pop(0)


def add_to_xab_x_natural_one_synth(emails: list[str], lenght: int, audio_files_correct: list[str], audio_files_wrong: list[str], accent_right: str, row_list: list[str]):
    """WARNING: legacy function, not being currently used for the article as of 2023-02-06. Only use if the article conditions change.
    
    Adds the given emails and audio files to the row list, that will be used to create the dataframe for the XAB test, 
    where the X audio is natural and one of a or b is natural, while the other is synthetic.

    Args:
        emails (list[str]): List of emails to be added to the row list. Please verify if the accent is condizent with the audio files and accent.
        lenght (int): Lenght of the test that is to be given to each student. Total row list size will be lenght * len(emails).
        audio_files_correct (list[str]): List of audio files with the right accent. Please verify if the accent is condizent with the emails.
        audio_files_wrong (list[str]): List of audio files with the wrong accent.
        accent_right (str): State acronym (lowercase) of the right accent.
        row_list (list[str]): List of rows to be added to the dataframe.
    """
    for i in range(lenght):
        if len(audio_files_correct) == 0 or len(audio_files_wrong) == 0 or i >= SYNTH_AMOUNT_XAB_PER_ACCENT:
            break
        rng = random.randint(0, 1)
        for email in emails:
            if rng == 0:
                row_list.append([email, audio_files_correct[0], audio_files_correct[1], audio_files_wrong[0][0],
                                  accent_right, accent_right, audio_files_wrong[0][1], 'n', ''])
            else:
                row_list.append([email, audio_files_correct[0], audio_files_wrong[0][0], audio_files_correct[1],
                                  accent_right, audio_files_wrong[0][1], accent_right, 'n', ''])
                
        audio_files_correct.pop(0)
        audio_files_correct.pop(1)
        audio_files_wrong.pop(0)


def add_to_xab_x_synth_two_natural(emails: list[str], lenght: int, audio_files_synth: list[str], audio_files_correct: list[str], audio_files_wrong: list[str], accent_right: str, row_list: list[str]):
    """WARNING: legacy function, not being currently used for the article as of 2023-02-06. Only use if the article conditions change.
    # go_path_synth
    Adds the given emails and audio files to the row list, that will be used to create the dataframe for the XAB test, 
    where the X audio is synthetic and both a and b are natural.

    Args:
        emails (list[str]): List of emails to be added to the row list. Please verify if the accent is condizent with the audio files and accent.
        lenght (int): Lenght of the test that is to be given to each student. Total row list size will be lenght * len(emails).
        audio_files_synth (list[str]): List of synthetic audio files. Please verify if the accent is condizent with the emails.
        audio_files_correct (list[str]): List of audio files with the right accent. Please verify if the accent is condizent with the emails.
        audio_files_wrong (list[str]): List of audio files with the wrong accent.
        accent_right (str): State acronym (lowercase) of the right accent.
        row_list (list[str]): List of rows to be added to the dataframe.
    """
    for i in range(lenght):
        if len(audio_files_synth) == 0 or len(audio_files_correct) == 0 or len(audio_files_wrong) == 0 or i >= SYNTH_AMOUNT_XAB_PER_ACCENT:
            break
        rng = random.randint(0, 1)
        for email in emails:
            if rng == 0:
                row_list.append([email, audio_files_synth[0], audio_files_correct[0], audio_files_wrong[0][0],
                                  accent_right, accent_right, audio_files_wrong[0][1], 's', ''])
            else:
                row_list.append([email, audio_files_synth[0], audio_files_wrong[0][0], audio_files_correct[0],
                                  accent_right, audio_files_wrong[0][1], accent_right, 's', ''])
                
        audio_files_synth.pop(0)
        audio_files_correct.pop(0)
        audio_files_wrong.pop(0)



# list of emails for each region
emails_al = [
    'juliogaldino@usp.br',
    'maryannehenrique@gmail.com',
    'eliel.costa@fale.ufal.br',
    'pedro.alencar@fale.ufal.br',
    'jin.gomes@fale.ufal.br',
    'guico21@usp.br',
]

emails_sp = [
    'jess.laureano@usp.br',
    'rianpf@usp.br',
    'gisellamatrone@usp.br',
    'thalesgmenis@usp.br',
    'leoishida@usp.br',
    'arnaldocan@gmail.com',
    'sandra@icmc.usp.br',
]

emails_go = [
]


# variables for the csv files being read
al_path = pandas.read_csv(my_path + "/metadata_coqui_bral_test.csv",
                     sep='\t', encoding='utf-8')
sp_path = pandas.read_csv(my_path + "/metadata_coqui_brsp_test.csv",
                     sep='\t', encoding='utf-8')


# variables for the synthetic audio files
# al_path_synth
# sp_path_synth


# creating the dataframes for the csv files
assignment_xab = pandas.DataFrame(columns=['email', 'audio_file_x', 'audio_file_a', 'audio_file_b', 
                                       'sotaque_x', 'sotaque_a', 'sotaque_b', 'natural', 'answer'])

assignment_mos = pandas.DataFrame(columns=['email', 'audio_file', 'natural', 'answer'])


# arrays with each audio path
al_path_arr = al_path['audio_file'].tolist()
al_path_arr = al_path_arr[:NATURAL_AMOUNT_TOTAL_PER_ACCENT]
sp_path_arr = sp_path['audio_file'].tolist()
sp_path_arr = sp_path_arr[:NATURAL_AMOUNT_TOTAL_PER_ACCENT]
# al_path_synth_arr = al_path_synth['audio_file'].tolist()
# sp_path_synth_arr = sp_path_synth['audio_file'].tolist()

for i in range(len(al_path_arr)):
    al_path_arr[i] = "http://143.107.183.175:14888/static/Dataset/" + al_path_arr[i]


for i in range(len(sp_path_arr)):
    sp_path_arr[i] = "http://143.107.183.175:14888/static/Dataset/" + sp_path_arr[i]


# randomize the path arrays
random.shuffle(al_path_arr)
random.shuffle(sp_path_arr)
# random.shuffle(al_path_synth_arr)
# random.shuffle(sp_path_synth_arr)


# list of rows to be added to the dataframe
row_list_xab = []
row_list_mos = []


# temp variable for testing
al_path_synth_arr = []
sp_path_synth_arr = []
synth_path_al = "/static/audio/al.wav"
synth_path_sp = "/static/audio/sp.wav"


# temp loops, remove later
for i in range(0, SYNTH_AMOUNT_TOTAL_PER_ACCENT):
    al_path_synth_arr.append(synth_path_al)
    sp_path_synth_arr.append(synth_path_sp)


synth_mos_arr = []
for i in range(0, SYNTH_AMOUNT_MOS_PER_ACCENT):
    synth_mos_arr.append(al_path_synth_arr.pop(0))
    synth_mos_arr.append(sp_path_synth_arr.pop(0))

natural_mos_arr = []
for i in range(0, NATURAL_AMOUNT_MOS_PER_ACCENT):
    natural_mos_arr.append(al_path_arr.pop(0))
    natural_mos_arr.append(sp_path_arr.pop(0))


# adding the rows to the lists
add_to_mos_list(emails_al + emails_sp, SYNTH_AMOUNT_MOS_PER_ACCENT * 2, synth_mos_arr, 's', row_list_mos)
add_to_mos_list(emails_al + emails_sp, NATURAL_AMOUNT_MOS_PER_ACCENT * 2, natural_mos_arr, 'n', row_list_mos)

random.shuffle(row_list_mos)
assignment_mos = pandas.DataFrame(row_list_mos, columns=['email', 'audio_file', 'natural', 'answer'])
create_csv(assignment_mos, my_path + '/assignment_mos.csv')


# reserve half of each xab list for the wrong answer
half_of_all_lists = []


# add more appends if more accents are ever added
for i in range(SYNTH_AMOUNT_XAB_PER_ACCENT // NUMBER_OF_ACCENTS):
    half_of_all_lists.append([al_path_synth_arr.pop(0), 'al'])
    half_of_all_lists.append([sp_path_synth_arr.pop(0), 'sp'])


# variables for the wrong answers for each accent
# add new lists if more accents are ever added
no_al_paths = []
no_sp_paths = []

# add more pops if more accents are ever added
while len(half_of_all_lists) > 0:
    if half_of_all_lists[0][1] != 'al':
        no_al_paths.append(half_of_all_lists.pop(0))
    elif half_of_all_lists[0][1] != 'sp':
        no_sp_paths.append(half_of_all_lists.pop(0))


# add xab tests
add_to_xab_x_natural_two_synth(emails_al + emails_sp, NATURAL_AMOUNT_XAB_PER_ACCENT, al_path_arr, al_path_synth_arr, no_al_paths, 'al', row_list_xab)
add_to_xab_x_natural_two_synth(emails_al + emails_sp, NATURAL_AMOUNT_XAB_PER_ACCENT, sp_path_arr, sp_path_synth_arr, no_sp_paths, 'sp', row_list_xab)


random.shuffle(row_list_xab)
assignment_xab = pandas.DataFrame(row_list_xab, columns=['email', 'audio_file_x', 'audio_file_a', 'audio_file_b',
                                                      'sotaque_x', 'sotaque_a', 'sotaque_b', 'natural', 'answer'])
create_csv(assignment_xab, my_path + '/assignment_xab.csv')
