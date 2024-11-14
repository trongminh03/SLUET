import os
import json
import argparse

def process_file(input_file_path, output_file_path): 
    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            # Parse the JSON object from the line
            json_data = json.loads(line.strip())
            
            # Extract sentence and entities
            # sentence = json_data["sentence"].replace("phòng thời", "phòng thờ")
            sentence = json_data["sentence"]
            entities = json_data["entities"]
            
            # Construct sentence_annotation from sentence and entities
            sentence_annotation = " " + sentence + " "
            processed_position = 0
            for entity in entities:
                entity_type = entity["type"]
                entity_filler = entity["filler"]
                # Replace entity placeholders in sentence with [entity_type : entity_filler]
                # sentence_annotation = sentence_annotation.replace(entity_filler, entity_type, 1)
                processed_part = sentence_annotation[:processed_position]
                unprocessed_part = sentence_annotation[processed_position:]
                unprocessed_part = unprocessed_part.replace(" " + entity_filler + " ", f" [ {entity_type} : {entity_filler} ] ", 1)
                sentence_annotation = processed_part + unprocessed_part
                
                # Update processed_position
                processed_position = processed_position + unprocessed_part.find(f" [ {entity_type} : {entity_filler} ] ") + len(f" [ {entity_type} : {entity_filler} ]")
                
            # for entity in entities:
            #     entity_type = entity["type"]
            #     entity_filler = entity["filler"]
            #     if f"[ {entity_type} : {entity_filler} ]" not in sentence_annotation:
            #         sentence_annotation = sentence_annotation.replace(entity_type, f"[ {entity_type} : {entity_filler} ]")


            # Add sentence_annotation to the JSON object
            json_data["sentence_annotation"] = sentence_annotation.strip()
            json_data["sentence"] = sentence
            # Write the updated JSON object to the output file
            output_file.write(json.dumps(json_data, ensure_ascii=False) + '\n')

def main(metadata_folder, output_folder): 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each JSONL file in the metadata folder and output to corresponding files in the output folder
    for file_name in ["train.jsonl", "test.jsonl", "dev.jsonl"]:
        input_file_path = os.path.join(metadata_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name)
        
        print(f"Processing {file_name}...")
        process_file(input_file_path, output_file_path)

    print(f'Processed files have been saved in {output_folder}')

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    # args.add_argument('-j', '--train_file', type=str, required = True,help='Path to train.jsonl file') 
    args.add_argument('-m', '--metadata_folder', type=str, required = True,help='Path to metadata folder') 
    args.add_argument('-o', '--output_folder', type=str, required = True,help='Path to output folder')
    args = args.parse_args()

    main(args.metadata_folder, args.output_folder)
