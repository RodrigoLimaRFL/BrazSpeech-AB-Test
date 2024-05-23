import pandas
import random
import os
from database import Database

my_path = os.path.abspath(os.path.dirname(__file__))

random.seed(1337)

NUMBER_OF_ACCENTS = 2

# OBS: THE VALUES FOR THE ARTICLE WILL BE 36, 12, 48
SYNTH_AMOUNT_XAB_PER_ACCENT = 36
SYNTH_AMOUNT_MOS_PER_ACCENT = 12
SYNTH_AMOUNT_TOTAL_PER_ACCENT = 48

# OBS: THE VALUES FOR THE ARTICLE WILL BE 18, 12, 30
NATURAL_AMOUNT_XAB_PER_ACCENT = 16
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
        if len(audio_files_correct) == 0 or len(audio_files_wrong) == 0 or i >= NATURAL_AMOUNT_XAB_PER_ACCENT:
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
        emails (list[str]): List of emails to be added to the row list.
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


def same_speaker(audio_file_a: str, audio_file_b: str):
    audio_file_a.split('/')
    audio_file_b.split('/')

    if len(audio_file_a) == 0 or len(audio_file_b) == 0:
        print("Error: audio file path is empty")
        return False
    
    return audio_file_a[7] == audio_file_b[7]


def add_to_xab_x_natural_two_natural_sp(emails: list[str], lenght: int, audio_files_sp: list[str], audio_files_al: list[str], row_list: list[str]):
    """Adds the given emails and audio files to the row list, that will be used to create the dataframe for the XAB test,
    where the X audio is natural and both a and b are natural.

    Args:
        emails (list[str]): List of emails to be added to the row list. 
        lenght (int): Lenght of the test that is to be given to each student. Total row list size will be lenght * len(emails).
        audio_files_sp(list[str]): List of audio files with the accent of the state of São Paulo. Please verify if the accent is condizent with the emails.
        audio_files_al(list[str]): List of audio files with the accent of the state of Alagoas. Please verify if the accent is condizent with the emails.
        row_list (list[str]): List of rows to be added to the dataframe.
    """

    given_sp_files = []
    given_al_files = []

    for i in range(lenght):
        random_sp_file = random.randint(0, audio_files_sp.__len__() - 1)

        given_sp_files.append(random_sp_file)

        second_sp_file = None

        while True:
            if second_sp_file is None or second_sp_file == random_sp_file:
                second_sp_file = random.randint(0, audio_files_sp.__len__() - 1)
                break

        given_sp_files.append(second_sp_file)

        random_al_file = random.randint(0, audio_files_al.__len__() - 1)

        given_al_files.append(random_al_file)

        second_al_file = None

        while True:
            if second_al_file is None or second_al_file == random_al_file:
                second_al_file = random.randint(0, audio_files_al.__len__() - 1)
                break

        given_al_files.append(second_al_file)

        rng = random.randint(0, 1)

        for email in emails:
            match rng:
                case 0:
                    row_list.append([email, audio_files_sp[random_sp_file], audio_files_sp[second_sp_file], 
                                     audio_files_al[random_al_file], 'sp', 'sp', 're', 'n', ''])
                case 1:
                    row_list.append([email, audio_files_sp[random_sp_file], audio_files_al[random_al_file], 
                                     audio_files_sp[second_sp_file], 'sp', 're', 'sp', 'n', ''])
                case _:
                    pass
        
        audio_files_sp.pop(random_sp_file)
        audio_files_sp.pop(second_sp_file)
        audio_files_al.pop(random_al_file)


def add_to_xab_x_natural_two_natural_al(emails: list[str], lenght: int, audio_files_sp: list[str], audio_files_al: list[str], row_list: list[str]):
    """Adds the given emails and audio files to the row list, that will be used to create the dataframe for the XAB test,

    Args:
        emails (list[str]): List of emails to be added to the row list.
        lenght (int): Lenght of the test that is to be given to each student. Total row list size will be lenght * len(emails).
        audio_files_sp (list[str]): List of audio files with the accent of the state of São Paulo. Please verify if the accent is condizent with the emails.
        audio_files_al (list[str]): List of audio files with the accent of the state of Alagoas. Please verify if the accent is condizent with the emails.
        row_list (list[str]): List of rows to be added to the dataframe.
    """

    given_sp_files = []
    given_al_files = []

    for i in range(lenght):
        random_sp_file = random.randint(0, audio_files_sp.__len__() - 1)

        given_sp_files.append(random_sp_file)

        second_sp_file = None

        while True:
            if second_sp_file is None or second_sp_file == random_sp_file:
                second_sp_file = random.randint(0, audio_files_sp.__len__() - 1)
                break

        given_sp_files.append(second_sp_file)

        random_al_file = random.randint(0, audio_files_al.__len__() - 1)

        given_al_files.append(random_al_file)

        second_al_file = None

        while True:
            if second_al_file is None or second_al_file == random_al_file:
                second_al_file = random.randint(0, audio_files_al.__len__() - 1)
                break
        
        given_al_files.append(second_al_file)

        rng = random.randint(0, 1)

        for email in emails:
            match rng:
                case 0:
                    row_list.append([email, audio_files_al[random_al_file], audio_files_al[second_al_file], 
                                     audio_files_sp[random_sp_file], 're', 're', 'sp', 'n', ''])
                case 1:
                    row_list.append([email, audio_files_al[random_al_file], audio_files_sp[random_sp_file], 
                                     audio_files_al[second_al_file], 're', 'sp', 're', 'n', ''])
                case _:
                    pass
        
        audio_files_sp.pop(random_sp_file)
        audio_files_sp.pop(second_sp_file)
        audio_files_al.pop(random_al_file)



def extract_name(s: str):
    # Find the position of the third underscore
    substring = s.split('/')[2]

    pos1 = substring.find('_')
    pos2 = substring.find('_', pos1 + 1)
    pos3 = substring.find('_', pos2 + 1)
    
    if pos3 == -1:
        return substring
    
    # Extract and return the substring between the third underscore and the forward slash
    return substring[pos3:]


def ensure_different_elements_by_swapping(list1, list2):
    n = min(len(list1), len(list2))
    
    for i in range(n):
        # If elements at the same index are the same
        if extract_name(list1[i]) == extract_name(list2[i]):
            # Find a new index to swap with that makes list2[i] different from list1[i]
            swap_index = i
            while swap_index == i or extract_name(list1[i]) == extract_name(list2[swap_index]):
                swap_index = random.randint(0, n-1)
            # Swap the elements in list2
            list2[i], list2[swap_index] = list2[swap_index], list2[i]
    
    return list1, list2


def add_to_xab_mupe(emails: list[str], lenght: int, audio_files_x: list[str], audio_files_a: list[str], audio_files_b: list[str], accent_right: str, accent_wrong: str, row_list: list[str]):
    """Adds the given emails and audio files to the row list, that will be used to create the dataframe for the XAB test,

    Args:
        emails (list[str]): List of emails to be added to the row list.
        lenght (int): Lenght of the test that is to be given to each student. Total row list size will be lenght * len(emails).
        audio_files_x (list[str]): List of audio files with the right accent. Please verify if the accent is condizent with the emails.
        audio_files_a (list[str]): List of audio files with the right accent. Please verify if the accent is condizent with the emails.
        audio_files_b (list[str]): List of audio files with the wrong accent.
        accent_right (str): State acronym (lowercase) of the right accent.
        accent_wrong (str): State acronym (lowercase) of the wrong accent.
        row_list (list[str]): List of rows to be added to the dataframe.
    """

    ensure_different_elements_by_swapping(audio_files_x, audio_files_a)

    for i in range(lenght):
        if len(audio_files_x) == 0 or len(audio_files_a) == 0 or len(audio_files_b) == 0:
            break

        rng = random.randint(0, 1)

        if(rng == 0):
            for email in emails:
                row_list.append([email, "http://143.107.183.175:14888/static/Dataset/" + audio_files_x[0], 
                                 "http://143.107.183.175:14888/static/Dataset/" + audio_files_a[0], 
                                 "http://143.107.183.175:14888/static/Dataset/" + audio_files_b[0],
                                  accent_right, accent_right, accent_wrong, 'n', ''])
        else:
            for email in emails:
                row_list.append([email, "http://143.107.183.175:14888/static/Dataset/" + audio_files_x[0], 
                                 "http://143.107.183.175:14888/static/Dataset/" + audio_files_b[0], 
                                 "http://143.107.183.175:14888/static/Dataset/" + audio_files_a[0],
                                  accent_right, accent_wrong, accent_right, 'n', ''])
                
        audio_files_x.pop(0)
        audio_files_a.pop(0)
        audio_files_b.pop(0)


#db = Database()
#version = db._run_query("SELECT VERSION()")
#print(f"Database version: {version}")

# list of emails for each region
emails_al = [
    'eliel.costa@false.ufal.br',
    'jin.gomes@fale.ufal.br',
    'joaosouza2@discente.ufg.br'
    'maryannehenrique@gmail.com',
    'pedro.alencar@fale.ufal.br',
    'test',
    
]

emails_sp = [
    'gisellamatrone@usp.br',
    'gustavowlopes@usp.br',
    'jess.laureano@usp.br',
    'leoishida@usp.br',
    'rianpf@usp.br',
    'thalesgmenis@usp.br',
    'guico21@usp.br',
    'arnaldocan@gmail.com',
    'sandra@icmc.usp.br',
]

emails_go = [
]

all_emails = [
    "eliel.costa@fale.ufal.br",
    "gisellamatrone@usp.br",
    "gustavowlopes@usp.br",
    "jess.laureano@usp.br",
    "jin.gomes@fale.ufal.br",
    "joaosouza2@discente.ufg.br",
    "leoishida@usp.br",
    "maryannehenrique@gmail.com",
    "pedro.alencar@fale.ufal.br",
    "rianpf@usp.br",
    "thalesgmenis@usp.br",
    "miguel@fale.ufal.br",
    "juliogaldino@usp.br",
    "giovana.meloni.craveiro@alumni.usp.br",
    "flavianesvartman@usp.br",
    "renan.izaias@usp.br",
    "carolalves@usp.br",
    "gustavo_evangelista@usp.br",
    "guico21@usp.br",
    "arnaldocan@gmail.com",
    "sandra@icmc.usp.br",
    "test"
]


# variables for the csv files being read
al_path = pandas.read_csv(my_path + "/metadata_coqui_bral.csv",
                     sep='\t', encoding='utf-8')
sp_path = pandas.read_csv(my_path + "/metadata_coqui_brsp.csv",
                     sep='\t', encoding='utf-8')


# variables for the synthetic audio files
# al_path_synth
# sp_path_synth


# creating the dataframes for the csv files
assignment_xab = pandas.DataFrame(columns=['email', 'audio_file_x', 'audio_file_a', 'audio_file_b', 
                                       'sotaque_x', 'sotaque_a', 'sotaque_b', 'natural', 'answer'])

assignment_mos = pandas.DataFrame(columns=['email', 'audio_file', 'natural', 'answer'])

#FiveSecondAudiosSP = db.fiveSecAudiosSP()['file_path'].tolist()
FiveSecondAudiosSP = []

for i in range(len(FiveSecondAudiosSP)):
    FiveSecondAudiosSP[i] = "http://143.107.183.175:14888/static/Dataset/" + FiveSecondAudiosSP[i]

def get_relative_paths(directory):
    relative_paths = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            relative_path = "/static/audio/NURC-RE_5-sec/" + filename
            relative_paths.append(relative_path)
    return relative_paths

FiveSecondAudiosRE = get_relative_paths('/home/rodrigo/Documents/GitHub/BrazSpeech-AB-Test/BrazSpeech_AB_Test/static/audio/NURC-RE_5-sec')

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
#add_to_xab_x_natural_two_synth(emails_al + emails_sp, NATURAL_AMOUNT_XAB_PER_ACCENT, al_path_arr, al_path_synth_arr, no_al_paths, 'al', row_list_xab)
#add_to_xab_x_natural_two_synth(emails_al + emails_sp, NATURAL_AMOUNT_XAB_PER_ACCENT, sp_path_arr, sp_path_synth_arr, no_sp_paths, 'sp', row_list_xab)
#add_to_xab_x_natural_two_natural(emails_al + emails_sp, NATURAL_AMOUNT_XAB_PER_ACCENT, sp_path_arr, al_path_arr, row_list_xab)
#add_to_xab_x_natural_two_natural_sp(emails_al + emails_sp, NATURAL_AMOUNT_XAB_PER_ACCENT, FiveSecondAudiosSP, FiveSecondAudiosRE, row_list_xab)
#add_to_xab_x_natural_two_natural_al(emails_al + emails_sp, NATURAL_AMOUNT_XAB_PER_ACCENT, FiveSecondAudiosSP, FiveSecondAudiosRE, row_list_xab)

MupeHomemSpXSp = [
    "data/mupe/PC_MA_HV014_Antonio Dantas/audios/0218_PC_MA_HV014_Antonio Dantas_875.063_902.798.wav",
    "data/mupe/PC_MA_HV265_Roberto_Rodrigues_Rios/audios/0220_PC_MA_HV265_Roberto_Rodrigues_Rios_1166.9209999999998_1193.094.wav",
    "data/mupe/Antonio Rodrigues Filho [nCPO__rTdnM]/Antonio Rodrigues Filho [nCPO__rTdnM]_7948.697_7969.983.wav",
    "data/mupe/PC_MA_HV264_Antonio_Carlos_da_Silva_Sales/audios/1098_PC_MA_HV264_Antonio_Carlos_da_Silva_Sales_6772.226_6797.317.wav",
    "data/mupe/PC_MA_HV221_Geraldo_Garducci_Junior/audios/1812_PC_MA_HV221_Geraldo Garducci Junior_10867.872_10894.807999999999.wav",
    "data/mupe/PC_MA_HV268_Eduardo_Santos_(Netinho)/audios/0653_PC_MA_HV268_Eduardo_Santos_(Netinho)_4419.039000000001_4445.072.wav",
    "data/mupe/PC_MA_HV144_Gilberto Dupas/audios/0606_PC_MA_HV144_Gilberto Dupas_4277.403_4296.549.wav",
    "data/mupe/PC_MA_HV228_Orlando_D'Agostinho/audios/0274_PC_MA_HV228_Orlando D'Agostinho_1231.46_1256.424.wav",
    "data/mupe/PC_MA_HV228_Orlando_D'Agostinho/audios/0274_PC_MA_HV228_Orlando D'Agostinho_1231.46_1256.424.wav",
    "data/mupe/PC_MA_HV251_Carlos_Laporta/audios/1000_PC_MA_HV251_Carlos Laporta_6087.536_6114.223.wav",
]

MupeHomemSpAbSp = [
    "data/mupe/PC_MA_HV221_Geraldo_Garducci_Junior/audios/1535_PC_MA_HV221_Geraldo Garducci Junior_9224.311_9254.057999999999.wav",
    "data/mupe/PC_MA_HV264_Antonio_Carlos_da_Silva_Sales/audios/0151_PC_MA_HV264_Antonio_Carlos_da_Silva_Sales_1090.2060000000001_1118.433.wav",
    "data/mupe/PC_MA_HV265_Roberto_Rodrigues_Rios/audios/0526_PC_MA_HV265_Roberto_Rodrigues_Rios_2609.577_2637.434.wav",
    "data/mupe/Antonio Rodrigues Filho [nCPO__rTdnM]/Antonio Rodrigues Filho [nCPO__rTdnM]_1990.333_2018.26.wav",
    "data/mupe/PC_MA_HV268_Eduardo_Santos_(Netinho)/audios/0535_PC_MA_HV268_Eduardo_Santos_(Netinho)_3666.243_3694.926.wav",
    "data/mupe/PC_MA_HV014_Antonio Dantas/audios/1535_PC_MA_HV014_Antonio Dantas_6927.232_6955.54.wav",
    "data/mupe/PC_MA_HV144_Gilberto Dupas/audios/0973_PC_MA_HV144_Gilberto Dupas_7016.933_7036.422.wav",
    "data/mupe/PC_MA_HV228_Orlando_D'Agostinho/audios/0938_PC_MA_HV228_Orlando D'Agostinho_4129.566_4156.513.wav",
    "data/mupe/PC_MA_HV251_Carlos_Laporta/audios/0737_PC_MA_HV251_Carlos Laporta_4533.328_4549.0560000000005.wav",
]

MupeHomemSpAbPe = [
    "data/mupe/PC_MA_HV221_Geraldo_Garducci_Junior/audios/1580_PC_MA_HV221_Geraldo Garducci Junior_9588.735999999999_9617.452.wav",
    "data/mupe/PC_MA_HV264_Antonio_Carlos_da_Silva_Sales/audios/0832_PC_MA_HV264_Antonio_Carlos_da_Silva_Sales_5357.589999999999_5382.352.wav",
    "data/mupe/PC_MA_HV265_Roberto_Rodrigues_Rios/audios/0493_PC_MA_HV265_Roberto_Rodrigues_Rios_2429.705_2455.539.wav",
    "data/mupe/PC_MA_HV268_Eduardo_Santos_(Netinho)/audios/0082_PC_MA_HV268_Eduardo_Santos_(Netinho)_648.572_674.098.wav",
    "data/mupe/PC_MA_HV014_Antonio Dantas/audios/1157_PC_MA_HV014_Antonio Dantas_5109.025_5129.062.wav",
]

MupeMulherSpXSp = [
    "data/mupe/PC_MA_HV238_Vânia_Bure/audios/2287_PC_MA_HV238_Vânia Bure_10018.242_10042.153.wav",
    "data/mupe/PC_MA_HV008_Cisele Ortiz/audios/1691_PC_MA_HV008_Cisele Ortiz_8393.02_8420.61.wav",
    "data/mupe/PC_MA_HV241_Maria_Jose_da_Silva_Carvalho/audios/1583_PC_MA_HV241_Maria_Jose_da_Silva_Carvalho_7151.715_7178.811000000001.wav",
    "data/mupe/Benedicta Gonçalves Pereira [w3EyLFJaII8]/Benedicta Gonçalves Pereira [w3EyLFJaII8]_6276.711_6304.86.wav",
    "data/mupe/PC_MA_HV009_Edileine Fonseca/audios/0888_PC_MA_HV009_Edileine Fonseca_3809.455_3831.873.wav",
    "data/mupe/PC_MA_HV020_Maria Helena dos Santos/audios/0084_PC_MA_HV020_Maria Helena dos Santos_427.463_448.635.wav",
    "data/mupe/Lourdes Alves de Souza [zbiXSNOIafs]/Lourdes Alves de Souza [zbiXSNOIafs]_1837.718_1863.307.wav",
    "data/mupe/PC_MA_HV239_Odette_Carvalho_de_Lima/audios/0183_PC_MA_HV239_Odette Carvalho de Lima_843.134_860.8.wav",
    "data/mupe/PC_MA_HV207_Maria_da_Glória_Cardia_de_Castro/audios/0086_PC_MA_HV207_Maria da Glória Cardia de Castro_427.328_447.09299999999996.wav",
]

MupeMulherSpAbSp = [
    "data/mupe/PC_MA_HV008_Cisele Ortiz/audios/0166_PC_MA_HV008_Cisele Ortiz_801.563_829.078.wav",
    "data/mupe/PC_MA_HV009_Edileine Fonseca/audios/1585_PC_MA_HV009_Edileine Fonseca_6607.045_6634.032.wav",
    "data/mupe/PC_MA_HV238_Vânia_Bure/audios/1847_PC_MA_HV238_Vânia Bure_7815.937_7838.657.wav",
    "data/mupe/Benedicta Gonçalves Pereira [w3EyLFJaII8]/Benedicta Gonçalves Pereira [w3EyLFJaII8]_7432.51_7459.462.wav",
    "data/mupe/PC_MA_HV020_Maria Helena dos Santos/audios/0655_PC_MA_HV020_Maria Helena dos Santos_2598.899_2614.709.wav",
    "data/mupe/PC_MA_HV241_Maria_Jose_da_Silva_Carvalho/audios/1093_PC_MA_HV241_Maria_Jose_da_Silva_Carvalho_4798.552000000001_4819.662.wav",
    "data/mupe/Lourdes Alves de Souza [zbiXSNOIafs]/Lourdes Alves de Souza [zbiXSNOIafs]_2562.158_2585.992.wav",
    "data/mupe/PC_MA_HV239_Odette_Carvalho_de_Lima/audios/1237_PC_MA_HV239_Odette Carvalho de Lima_5712.792_5731.661.wav",
    "data/mupe/PC_MA_HV207_Maria_da_Glória_Cardia_de_Castro/audios/1588_PC_MA_HV207_Maria da Glória Cardia de Castro_9101.425000000001_9124.172.wav",
]

MupeMulherSpAbPe = [
    "data/mupe/PC_MA_HV008_Cisele Ortiz/audios/0829_PC_MA_HV008_Cisele Ortiz_4012.248_4039.768.wav",
    "data/mupe/PC_MA_HV009_Edileine Fonseca/audios/0965_PC_MA_HV009_Edileine Fonseca_4136.088_4156.532.wav",
    "data/mupe/PC_MA_HV238_Vânia_Bure/audios/2461_PC_MA_HV238_Vânia Bure_10921.952000000001_10945.057.wav",
    "data/mupe/Benedicta Gonçalves Pereira [w3EyLFJaII8]/Benedicta Gonçalves Pereira [w3EyLFJaII8]_1357.773_1376.562.wav",
    "data/mupe/PC_MA_HV241_Maria_Jose_da_Silva_Carvalho/audios/1280_PC_MA_HV241_Maria_Jose_da_Silva_Carvalho_5692.459000000001_5710.689.wav",
    "data/mupe/Lourdes Alves de Souza [zbiXSNOIafs]/Lourdes Alves de Souza [zbiXSNOIafs]_5360.347_5384.845.wav",
]

MupeHomemPeXPe = [
    "data/mupe/PC_MA_HV250_Severino_José_de_Albuquerque/audios/0724_PC_MA_HV250_Severino José de Albuquerque_3526.198_3552.0449999999996.wav",
    "data/mupe/PC_MA_HV211_Sebastião_Biano/audios/0800_PC_MA_HV211_Sebastião Biano_3731.645_3759.954.wav",
    "data/mupe/PC_MA_HV187_Antonio de Amorim Costa/audios/1098_PC_MA_HV187_Antonio de Amorim Costa_6389.062_6417.922.wav",
    "data/mupe/Gustavo Laureano da Silva/audios/0000_Gustavo Laureano da Silva_7.87_36.70.wav",
    "data/mupe/PC_MA_HV243_Euro_Ribeiro_da_Silva/audios/0161_PC_MA_HV243_Euro_Ribeiro_da_Silva_850.6510000000001_875.35.wav"
]

MupeHomemPeAbPe = [
    "data/mupe/PC_MA_HV211_Sebastião_Biano/audios/1074_PC_MA_HV211_Sebastião Biano_5172.655000000001_5196.613.wav",
    "data/mupe/PC_MA_HV250_Severino_José_de_Albuquerque/audios/0699_PC_MA_HV250_Severino José de Albuquerque_3378.79_3407.8689999999997.wav",
    "data/mupe/PC_MA_HV243_Euro_Ribeiro_da_Silva/audios/0893_PC_MA_HV243_Euro_Ribeiro_da_Silva_4509.562_4533.8279999999995.wav",
    "data/mupe/PC_MA_HV187_Antonio de Amorim Costa/audios/1013_PC_MA_HV187_Antonio de Amorim Costa_5937.125_5963.158.wav",
    "data/mupe/Gustavo Laureano da Silva/audios/0044_Gustavo Laureano da Silva_232.64_248.83.wav",
]

MupeHomemPeAbSp = [
    "data/mupe/PC_MA_HV250_Severino_José_de_Albuquerque/audios/0250_PC_MA_HV250_Severino José de Albuquerque_1232.33_1257.895.wav",
    "data/mupe/PC_MA_HV211_Sebastião_Biano/audios/0449_PC_MA_HV211_Sebastião Biano_2151.067_2173.047.wav",
    "data/mupe/PC_MA_HV211_Sebastião_Biano/audios/0859_PC_MA_HV211_Sebastião Biano_3987.879_4014.882.wav",
    "data/mupe/PC_MA_HV211_Sebastião_Biano/audios/1043_PC_MA_HV211_Sebastião Biano_5034.21_5052.5960000000005.wav",
    "data/mupe/PC_MA_HV187_Antonio de Amorim Costa/audios/0698_PC_MA_HV187_Antonio de Amorim Costa_3975.469_3992.017.wav",
    "data/mupe/PC_MA_HV187_Antonio de Amorim Costa/audios/0348_PC_MA_HV187_Antonio de Amorim Costa_1958.458_1977.968.wav",
    "data/mupe/PC_MA_HV243_Euro_Ribeiro_da_Silva/audios/1200_PC_MA_HV243_Euro_Ribeiro_da_Silva_6098.094_6115.367.wav",
    "data/mupe/Gustavo Laureano da Silva/audios/0039_Gustavo Laureano da Silva_193.35_205.95.wav",
    "data/mupe/Gustavo Laureano da Silva/audios/0042_Gustavo Laureano da Silva_218.77_230.32.wav",
]

MupeMulherPeXPe = [
    "data/mupe/PC_MA_HV047_Valéria Pereira Fagundes/audios/1365_PC_MA_HV047_Valéria Pereira Fagundes_5707.34_5736.80.wav",
    "data/mupe/Maria Martinha Torres/audios/0417_Maria Martinha Torres_1795.54_1818.65.wav",
    "data/mupe/PC_MA_HV245_Maria_Jose_da_Silva/audios/0065_PC_MA_HV245_Maria_Jose_da_Silva_281.35299999999995_307.31199999999995.wav",
    "data/mupe/PC_MA_HV146_Raquel Trindade de Souza/audios/0693_PC_MA_HV146_Raquel Trindade de Souza_3983.95_4012.38.wav",
    "data/mupe/PC_MA_HV266_Cristina_Rodrigues_de_Souza/audios/2229_PC_MA_HV266_Cristina_Rodrigues_de_Souza_6849.753_6871.6179999999995.wav",
    "data/mupe/PC_MA_HV197_Maria Almeida de Araujo Pessoa/audios/0727_PC_MA_HV197_Maria Almeida de Araujo Pessoa_2969.05_2985.43.wav",
]

MupeMulherPeAbPe = [
    "data/mupe/PC_MA_HV047_Valéria Pereira Fagundes/audios/1165_PC_MA_HV047_Valéria Pereira Fagundes_4891.34_4914.13.wav",
    "data/mupe/Maria Martinha Torres/audios/0665_Maria Martinha Torres_2977.91_3002.32.wav",
    "data/mupe/PC_MA_HV245_Maria_Jose_da_Silva/audios/0689_PC_MA_HV245_Maria_Jose_da_Silva_3199.759_3223.577.wav",
    "data/mupe/PC_MA_HV146_Raquel Trindade de Souza/audios/0873_PC_MA_HV146_Raquel Trindade de Souza_5247.61_5275.49.wav",
    "data/mupe/PC_MA_HV266_Cristina_Rodrigues_de_Souza/audios/1401_PC_MA_HV266_Cristina_Rodrigues_de_Souza_4156.007_4171.632.wav",
    "data/mupe/PC_MA_HV197_Maria Almeida de Araujo Pessoa/audios/0256_PC_MA_HV197_Maria Almeida de Araujo Pessoa_1040.67_1054.39.wav",
]

MupeMulherPeAbSp = [
    "data/mupe/Maria Martinha Torres/audios/0459_Maria Martinha Torres_2054.73_2074.20.wav",
    "data/mupe/PC_MA_HV245_Maria_Jose_da_Silva/audios/0878_PC_MA_HV245_Maria_Jose_da_Silva_4315.5070000000005_4338.834.wav",
    "data/mupe/PC_MA_HV245_Maria_Jose_da_Silva/audios/0924_PC_MA_HV245_Maria_Jose_da_Silva_4538.558_4560.086.wav",
    "data/mupe/PC_MA_HV047_Valéria Pereira Fagundes/audios/1399_PC_MA_HV047_Valéria Pereira Fagundes_5882.39_5906.03.wav",
    "data/mupe/Maria Martinha Torres/audios/0701_Maria Martinha Torres_3159.54_3177.94.wav",
    "data/mupe/PC_MA_HV047_Valéria Pereira Fagundes/audios/0657_PC_MA_HV047_Valéria Pereira Fagundes_2510.04_2535.99.wav",
    "data/mupe/PC_MA_HV266_Cristina_Rodrigues_de_Souza/audios/1919_PC_MA_HV266_Cristina_Rodrigues_de_Souza_5867.052_5883.584.wav",
    "data/mupe/PC_MA_HV146_Raquel Trindade de Souza/audios/0098_PC_MA_HV146_Raquel Trindade de Souza_627.07_652.71.wav",
    "data/mupe/PC_MA_HV197_Maria Almeida de Araujo Pessoa/audios/0773_PC_MA_HV197_Maria Almeida de Araujo Pessoa_3163.14_3177.80.wav"
]

random.shuffle(MupeHomemSpXSp)
random.shuffle(MupeHomemSpAbSp)
random.shuffle(MupeHomemSpAbPe)
random.shuffle(MupeMulherSpXSp)
random.shuffle(MupeMulherSpAbSp)
random.shuffle(MupeMulherSpAbPe)
random.shuffle(MupeHomemPeXPe)
random.shuffle(MupeHomemPeAbPe)
random.shuffle(MupeHomemPeAbSp)
random.shuffle(MupeMulherPeXPe)
random.shuffle(MupeMulherPeAbPe)
random.shuffle(MupeMulherPeAbSp)

add_to_xab_mupe(all_emails, len(MupeHomemPeXPe), MupeHomemPeXPe, MupeHomemPeAbPe, MupeHomemSpAbPe, 'pe', 'sp', row_list_xab)
add_to_xab_mupe(all_emails, len(MupeMulherPeAbPe), MupeMulherPeXPe, MupeMulherPeAbPe, MupeMulherSpAbPe, 'pe', 'sp', row_list_xab)
add_to_xab_mupe(all_emails, len(MupeHomemSpXSp), MupeHomemSpXSp, MupeHomemSpAbSp, MupeHomemPeAbSp, 'sp', 'pe', row_list_xab)
add_to_xab_mupe(all_emails, len(MupeMulherSpXSp), MupeMulherSpXSp, MupeMulherSpAbSp, MupeMulherPeAbSp, 'sp', 'pe', row_list_xab)

#random.shuffle(row_list_xab)
assignment_xab = pandas.DataFrame(row_list_xab, columns=['email', 'audio_file_x', 'audio_file_a', 'audio_file_b',
                                                      'sotaque_x', 'sotaque_a', 'sotaque_b', 'natural', 'answer'])
create_csv(assignment_xab, my_path + '/assignment_xab.csv')
