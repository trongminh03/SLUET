import subprocess
import argparse

def run_command(command): 
    subprocess.run(command, check=True)

# TRAIN_FILE_PATH = 'slu_data_1/data-process/train_processed.jsonl'
# AUGMENTED_TRAIN_FILE_PATH = 'slu_data_1/data-process/augmented_data.jsonl'
# INPUT_AUGMENTED_DATA = 'slu_data_1/data-process/random_sentences.jsonl' 

OUTPUT_FOLDER_PATH = 'slu_data/processed_output'

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-m', '--metadata_folder', type=str,required = True,help='Path to metadata folder')
    args.add_argument("--augment_data", action="store_true", help="Enable my augmented data")
    args = args.parse_args()
    # train_file_path = args.train_file 
    

    commands = [
        ["python", "slu_data/data-process/pre_process.py", "-m", args.metadata_folder, "-o", OUTPUT_FOLDER_PATH],
        ["python", "slu_data/data-process/in_label_convert.py"],
        ["python", "slu_data/data-process/out_convert.py"],
        # ["python", "slu_data/data-process/split.py"],
        ["python", "slu_data/data-process/vocab_process.py"]
    ]

    # if args.augment_data:
    #     commands.insert(0, ["python", "slu_data_1/data-process/generate_sentence.py"]) 
    #     commands.insert(1, ["python", "slu_data_1/data-process/pre_process.py", "-j", INPUT_AUGMENTED_DATA, "-o", AUGMENTED_TRAIN_FILE_PATH]) 
    #     commands[3].append("--augment_data")
    #     commands[4].append("--augment_data")
    #     commands[5].append("--augment_data")

    for command in commands:
        # print(command)
        run_command(command)