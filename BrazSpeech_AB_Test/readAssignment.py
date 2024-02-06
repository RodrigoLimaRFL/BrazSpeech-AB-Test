import pandas
import os


my_path = os.path.abspath(os.path.dirname(__file__))


dataset_mos = pandas.read_csv(my_path + '/csv/assignment_mos.csv')
dataset_xab = pandas.read_csv(my_path + '/csv/assignment_xab.csv')


def get_mos_audio(email: str, index: int) -> str:
    """Gets the audio file name for the specified email and local index.

    Args:
        email (str): Email of the user.
        index (int): Starts at 1. The local index of the audio file for the specified email.

    Returns:
        str: The audio file path.
    """
    return (dataset_mos.loc[dataset_mos['email'] == email].iloc[index - 1])['audio_file']


def get_mos_total(email:str) -> int:
    """Gets the total number of audio files for the specified email.

    Args:
        email (str): Email of the user.

    Returns:
        int: The total number of audio files for the specified email.
    """
    return len(dataset_mos.loc[dataset_mos['email'] == email])


def get_xab_audio_x(email: str, index: int) -> str:
    """Gets the audio file x name for the specified email and local index.

    Args:
        email (str): Email of the user.
        index (int): Starts at 1. The local index of the audio file for the specified email.
    
    Returns:
        str: The audio file path.
    """
    return (dataset_xab.loc[dataset_xab['email'] == email].iloc[index - 1])["audio_file_x"]


def get_xab_audio_a(email: str, index: int) -> str:
    """Gets the audio file a name for the specified email and local index.

    Args:
        email (str): Email of the user.
        index (int): Starts at 1. The local index of the audio file for the specified email.
    
    Returns:
        str: The audio file path.
    """
    return (dataset_xab.loc[dataset_xab['email'] == email].iloc[index - 1])["audio_file_a"]


def get_xab_audio_b(email: str, index: int) -> str:
    """Gets the audio file b name for the specified email and local index.

    Args:
        email (str): Email of the user.
        index (int): Starts at 1. The local index of the audio file for the specified email.
    
    Returns:
        str: The audio file path.
    """
    return (dataset_xab.loc[dataset_xab['email'] == email].iloc[index - 1])["audio_file_b"]


def get_xab_total(email: str) -> int:
    """Gets the total number of audio files for the specified email.

    Args:
        email (str): Email of the user.

    Returns:
        int: The total number of audio files for the specified email.
    """
    return len(dataset_xab.loc[dataset_xab['email'] == email])

def set_mos_answer(email: str, index: int, answer: int):
    """Sets the answer of the MOS test for the specified email and local index.

    Args:
        email (str): Email of the user.
        index (int): Starts at 1. The local index of the audio file for the specified email.
        answer (int): Ranges from 1 (inclusive) to 5 (inclusive). The answer to the MOS test.
    """
    # Locate the rows with the specified email
    indices = dataset_mos.index[(dataset_mos['email'] == email)]
    
    # Ensure the specified local index is within the range of rows with the same email
    if index - 1 < len(indices):
        # Set the answer in the specified row and column
        dataset_mos.loc[indices[index-1], 'answer'] = answer
        print(dataset_mos)
        
        # Save the modified DataFrame back to the CSV file
        dataset_mos.to_csv(my_path + '/csv/assignment_mos.csv', index=False)

def set_xab_answer(email: str, index: int, answer: str):
    """Sets the answer of the XAB test for the specified email and local index.

    Args:
        email (str): Email of the user.
        index (int): Starts at 1. The local index of the audio file for the specified email.
        answer (str): 'a' or 'b'. The answer to the XAB test.
    """
    # Locate the rows with the specified email
    indices = dataset_xab.index[(dataset_xab['email'] == email)]
    
    # Ensure the specified local index is within the range of rows with the same email
    if index - 1 < len(indices):
        # Set the answer in the specified row and column
        dataset_xab.loc[indices[index-1], 'answer'] = answer
        print(dataset_xab)
        
        # Save the modified DataFrame back to the CSV file
        dataset_xab.to_csv(my_path + '/csv/assignment_xab.csv', index=False)