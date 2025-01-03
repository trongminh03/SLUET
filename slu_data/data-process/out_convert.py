import os
import re
import json
import argparse 
import constants

def label_tokens(text):
    labels = []
    text = text.replace('_', ' ')
    matches = re.finditer(r'\[ ([^:]+) : ([^\]]+) \]', text)
    last_end = 0
    number = 0

    for match in matches:
        start = match.start(2)
        end = match.end(2)
        label_type = match.group(1)
        label_type = label_type.replace(' ', '_')
        num_underscores = label_type.count('_')
        label_value = match.group(2)

        # import IPython; IPython.embed()

        # Tokelabel_typetside the brackets and on the right side of the brackets
        if (number == 0):
            labels.extend(['O'] * (len(text[last_end:start].split()) - 3 - num_underscores))
            number += 1
        else:
            labels.extend(['O'] * (len(text[last_end:start].split()) - 4 - num_underscores))

        labels.extend(['B-' + label_type] + ['I-' + label_type] * (len(label_value.split()) - 1))
        last_end = end 
    # Tokenize remaining words
    if number == 0:
        labels.extend(['O'] * (len(text[last_end:].split())))
    else:

        labels.extend(['O'] * (len(text[last_end:].split()) - 1))
    
    return labels

def out_converter(file_path, annotation_path): 
    # Read data from the JSONL file
    data = []
    with open(file_path, 'r', encoding='utf-8') as jsonl_file:
        for line in jsonl_file:
            entry = json.loads(line)
            data.append(entry)

    with open(annotation_path, 'w', encoding='utf-8') as output_file:
        for entry in data:
            sentence_annotation = entry['sentence_annotation']
            modified_seq = sentence_annotation.replace(',', ' ')
            modified_seq = modified_seq.replace(']', ' ] ')
            modified_seq = modified_seq.replace('[', ' [')
            modified_seq = modified_seq.replace('\'',' ')
            modified_seq = modified_seq.replace('.',' ')
            modified_seq = modified_seq.replace('?', ' ')
            modified_seq = modified_seq.replace('!',' ')
            modified_seq = modified_seq.replace('/',' ')

            # import IPython; IPython.embed()

            labels = label_tokens(modified_seq)
            
            for label in labels:
                output_file.write(f"{label} ")
            output_file.write('\n')  

def main(data_folder): 
    for file_name in ["train.jsonl", "test.jsonl", "dev.jsonl"]:
        input_file_path = os.path.join(data_folder, file_name)
        annotation_path = os.path.join(constants.SYLLABLE_FOLDER, file_name.split('.')[0], "seq.out")
        out_converter(input_file_path, annotation_path)
    
    print("Label sequences generated and saved to 'seq.out'")

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--augment_data", action="store_true", help="Enable my augmented data")
    args = args.parse_args()

    # out_converter(constants.TRAIN_FILE_PATH, constants.ANNOTATION_PATH) 
    main(constants.OUTPUT_FOLDER_PATH)

    # Later
    # if args.augment_data: 
    #     out_converter(constants.AUGMENTED_TRAIN_FILE_PATH, constants.AUGMENTED_ANNOTATION_PATH)
    
    # print("Label sequences generated and saved to 'seq.out'")
