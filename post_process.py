import re
import json
import argparse
import zipfile

def process_line(line, filename):
    parts = line.strip().split(" -> ")
    intent = parts[0][1:-1]  # Remove angle brackets from the intent
    if (len(parts) == 1):
        return {"intent": uppercase_first_character(intent), "entities": [], "file":filename}
    entities = re.findall(r'\[(.*?)\]', parts[1])
    processed_entities = []
    current_entity = {}
    entity_filler = ""
    for entity in entities:
        entity_parts = entity.split(":")
        
        if len(entity_parts) >= 2:
            entity_type_parts = entity_parts[1].split("-")
            if len(entity_type_parts) >= 2:

                if entity_type_parts[0] == "B":
                    if current_entity != {}:
                        processed_entities.append(current_entity)
                        current_entity = {}
                        entity_filler = ""
                
                entity_type = entity_type_parts[1]
                filler = entity_parts[0]
                if entity_filler == "":
                    entity_filler = filler
                else:
                    entity_filler = entity_filler + " " + filler
                current_entity = {"type": entity_type, "filler": entity_filler}
    if current_entity != {}:
        processed_entities.append(current_entity)

    for entity in processed_entities:
        filler = entity['filler']
        filler = re.sub(r"(\d+)\s+km", r"\1km", filler)
        filler = re.sub(r"(\d+)\s+s", r"\1s", filler)
        entity['filler'] = filler
    return {"intent": intent, "entities": processed_entities, "file":filename}

def uppercase_first_character(input):
    first_character = input[0]
    upper_first_character = first_character.upper()
    return upper_first_character + input[1:]



def zip_file(input_file, output_zip):
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(input_file, arcname=input_file.split("/")[-1])
        print(f"{input_file} has been successfully zipped to {output_zip}")
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


zip_filename = 'Submission'

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-i', '--input_file', type=str, required = True,help='Path to output.txt file')
    args.add_argument('-t', '--wav_urls', type=str, required = True,help='Path to transcript.txt file')
    args.add_argument('-o', '--output_file', type=str, required = True,help='Predictions.jsonl file') 
    args = args.parse_args()

    input_filename = args.input_file
    wav_urls_filename = args.wav_urls
    output_filename = args.output_file

    filenames=[]
    with open(wav_urls_filename, 'r', encoding="utf-8") as wav_urls_file:
        wav_urls = wav_urls_file.readlines()

    for wav in wav_urls:
        filename = re.findall(r'/(\w+\.wav)', wav)[0]
        filenames.append(filename)


    with open(input_filename, "r", encoding="utf-8") as input_file, open(output_filename, "w", encoding="utf-8") as output_file:
        for line, filename in zip(input_file, filenames):
            jsonline = process_line(line, filename)
            output_file.write(json.dumps(jsonline, ensure_ascii=False) + "\n")
            # result = format(jsonline)
            # output_file.write(json.dumps(result, ensure_ascii=False) + "\n")
    
    zip_file(output_filename, zip_filename + ".zip")