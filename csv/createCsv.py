import pandas
import random
import os

my_path = os.path.abspath(os.path.dirname(__file__))

random.seed(1337)


def create_csv(dataframe: pandas.DataFrame, path: str):
    """Creates a csv file with the given dataframe

    Args:
        dataframe (pandas.DataFrame): Dataframe to be written to the csv file
        path (str): Path to the csv file. Must include the file name and extension.
    """
    dataframe.sort_values(by=['email'], inplace=True)

    dataframe.to_csv(path, index=False)


def add_to_mos_list(emails: list[str], lenght: int, audio_files: list[str], row_list: list[str]):
    """Adds the given emails and audio files to the row list, that will be used to create the dataframe for the MOS test

    Args:
        emails (list[str]): List of emails to be added to the row list. Please verify if the accent is condizent with the audio files.
        lenght (int): Lenght of the test that is to be given to each student. Total row list size will be lenght * len(emails)
        audio_files (list[str]): List of audio files to be added to the row list. Please verify if the accent is condizent with the emails.
        row_list (list[str]): List of rows to be added to the dataframe
    """
    for i in range(lenght):
        if len(audio_files) == 0:
            break
        for email in emails:
            row_list.append([email, audio_files[0], ''])
        audio_files.pop(0)


def add_to_xab_natural(emails: list[str], lenght: int, audio_files_correct: list[str], audio_files_wrong: list[str], accent_right: str, row_list: list[str]):
    """Adds the given emails and audio files to the row list, that will be used to create the dataframe for the XAB test, where the X audio is natural.

    Args:
        emails (list[str]): List of emails to be added to the row list. Please verify if the accent is condizent with the audio files and accent.
        lenght (int): Lenght of the test that is to be given to each student. Total row list size will be lenght * len(emails).
        audio_files_correct (list[str]): List of audio files with the right accent. Please verify if the accent is condizent with the emails.
        audio_files_wrong (list[str]): List of audio files with the wrong accent.
        accent_right (str): State acronym (lowercase) of the right accent.
        row_list (list[str]): List of rows to be added to the dataframe.
    """
    for i in range(lenght):
        if len(audio_files_correct) == 0 or len(audio_files_wrong) == 0:
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


def add_to_xab_synth(emails: list[str], lenght: int, audio_files_synth: list[str], audio_files_correct: list[str], audio_files_wrong: list[str], accent_right: str, row_list: list[str]):
    """WARNING: legacy function, not being currently used for the article as of 2023-02-06. Only use if the article conditions change.
    
    Adds the given emails and audio files to the row list, that will be used to create the dataframe for the XAB test, where the X audio is synthetic.

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
        if len(audio_files_synth) == 0 or len(audio_files_correct) == 0 or len(audio_files_wrong) == 0:
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
]

emails_go = [
    'joaosouza2@discente.ufg.br',
    'arnaldocan@gmail.com',
    'sandra@icmc.usp.br',
]


# variables for the csv files being read
al_path = pandas.read_csv(my_path + "/metadata_coqui_bral_test.csv",
                     sep='\t', encoding='utf-8')
go_path = pandas.read_csv(my_path + "/metadata_coqui_brgo_test.csv",
                     sep='\t', encoding='utf-8')
sp_path = pandas.read_csv(my_path + "/metadata_coqui_brsp_test.csv",
                     sep='\t', encoding='utf-8')


# variables for the synthetic audio files
# al_path_synth
# go_path_synth
#  sp_path_synth


# creating the dataframes for the csv files
assignment_xab = pandas.DataFrame(columns=['email', 'audio_file_x', 'audio_file_a', 'audio_file_b', 
                                       'sotaque_x', 'sotaque_a', 'sotaque_b', 'natural', 'answer'])

assignment_mos = pandas.DataFrame(columns=['email', 'audio_file', 'answer'])


# arrays with each audio path
al_path_arr = al_path['audio_file'].tolist()
go_path_arr = go_path['audio_file'].tolist()
sp_path_arr = sp_path['audio_file'].tolist()
# al_path_synth_arr = al_path_synth['audio_file'].tolist()
# go_path_synth_arr = go_path_synth['audio_file'].tolist()
# sp_path_synth_arr = sp_path_synth['audio_file'].tolist()

for i in range(len(al_path_arr)):
    al_path_arr[i] = "http://143.107.183.175:14888/static/Dataset/" + al_path_arr[i]

for i in range(len(go_path_arr)):
    go_path_arr[i] = "http://143.107.183.175:14888/static/Dataset/" + go_path_arr[i]

for i in range(len(sp_path_arr)):
    sp_path_arr[i] = "http://143.107.183.175:14888/static/Dataset/" + sp_path_arr[i]


# randomize the path arrays
random.shuffle(al_path_arr)
random.shuffle(go_path_arr)
random.shuffle(sp_path_arr)
# random.shuffle(al_path_synth_arr)
# random.shuffle(go_path_synth_arr)
# random.shuffle(sp_path_synth_arr)


# list of rows to be added to the dataframe
row_list_xab = []
row_list_mos = []


# temp variable for testing
al_path_synth_arr = []
go_path_synth_arr = []
sp_path_synth_arr = []
synth_path = "/static/audio/audio_x.wav"


# temp loops, remove later
for i in range(0, 100):
    al_path_synth_arr.append(synth_path)
    go_path_synth_arr.append(synth_path)
    sp_path_synth_arr.append(synth_path)

print(len(al_path_arr))


# dividing the original size of the arrays by 5 so we can have 5 equal portions
al_one_fifth_original_size = len(al_path_arr) // 5
go_one_fifth_original_size = len(go_path_arr) // 5
sp_one_fifth_original_size = len(sp_path_arr) // 5


print(al_one_fifth_original_size)


# adding the rows to the lists
add_to_mos_list(emails_al, al_one_fifth_original_size, al_path_synth_arr, row_list_mos)
add_to_mos_list(emails_go, go_one_fifth_original_size, go_path_synth_arr, row_list_mos)
add_to_mos_list(emails_sp, sp_one_fifth_original_size, sp_path_synth_arr, row_list_mos)


assignment_mos = pandas.DataFrame(row_list_mos, columns=['email', 'audio_file', 'answer'])
create_csv(assignment_mos, my_path + '/assignment_mos.csv')


no_al_paths = []
no_go_paths = []
no_sp_paths = []


for i in range(al_one_fifth_original_size):
    no_al_paths.append([go_path_arr.pop(0), 'go'])
    no_al_paths.append([sp_path_arr.pop(0), 'sp'])


for i in range(go_one_fifth_original_size):
    no_go_paths.append([al_path_arr.pop(0), 'al'])
    no_go_paths.append([sp_path_arr.pop(0), 'sp'])

for i in range(sp_one_fifth_original_size):
    no_sp_paths.append([al_path_arr.pop(0), 'al'])
    no_sp_paths.append([go_path_arr.pop(0), 'go'])

print(len(al_path_arr))

# add natural test to xab
add_to_xab_natural(emails_al, al_one_fifth_original_size, al_path_arr, no_al_paths, 'al', row_list_xab)
add_to_xab_natural(emails_go, go_one_fifth_original_size, go_path_arr, no_go_paths, 'go', row_list_xab)
add_to_xab_natural(emails_sp, sp_one_fifth_original_size, sp_path_arr, no_sp_paths, 'sp', row_list_xab)

print(len(al_path_arr))

# add synthetic test to xab
add_to_xab_synth(emails_al, al_one_fifth_original_size, al_path_synth_arr, al_path_arr, no_al_paths, 'al', row_list_xab)
add_to_xab_synth(emails_go, go_one_fifth_original_size, go_path_synth_arr, go_path_arr, no_go_paths, 'go', row_list_xab)
add_to_xab_synth(emails_sp, sp_one_fifth_original_size, sp_path_synth_arr, sp_path_arr, no_sp_paths, 'sp', row_list_xab)

random.shuffle(row_list_xab)
assignment_xab = pandas.DataFrame(row_list_xab, columns=['email', 'audio_file_x', 'audio_file_a', 'audio_file_b',
                                                      'sotaque_x', 'sotaque_a', 'sotaque_b', 'natural', 'answer'])
create_csv(assignment_xab, my_path + '/assignment_xab.csv')
