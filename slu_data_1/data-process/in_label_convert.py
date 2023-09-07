import json
# Read the JSONL file
with open('./augmented_data.jsonl', 'r', encoding='utf-8') as jsonl_file:
    intents = []
    sentences = []
    for line in jsonl_file:
        entry = json.loads(line)
        
        intent = entry['intent']
        sentence = entry['sentence']
        intents.append(intent)
        sentences.append(sentence)

# Write intents to the label file
with open('./augmented_label', 'w', encoding='utf-8') as label_file:
    for intent in intents:
        label_file.write(intent + '\n')
        
with open('./augmented_seq.in', 'w', encoding='utf-8') as in_file:
    for seq in sentences:
        modified_seq = seq.replace(',', ' ')
        modified_seq = modified_seq.replace(']', ' ] ')
        modified_seq = modified_seq.replace('\'',' ')
        modified_seq = modified_seq.replace('.',' ')
        modified_seq = modified_seq.replace('?', ' ')
        modified_seq = modified_seq.replace('!',' ')
        modified_seq = modified_seq.replace('/',' ')
        modified_seq.strip()
        in_file.write(modified_seq + '\n')
        

print("Intents extracted and saved to 'label and seq.in'")
