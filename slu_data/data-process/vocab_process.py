import os

def vocab_process(data_dir):
    slot_label_vocab = "slot_label.txt"
    intent_label_vocab = "intent_label.txt"

    # Initialize vocab sets to collect unique labels across all files
    intent_vocab = set()
    slot_vocab = set()

    # Process each split (train, test, dev) for intents and slots
    for split in ["train", "test", "dev"]:
        split_dir = os.path.join(data_dir, split)

        # Intent labels
        with open(os.path.join(split_dir, "label"), "r", encoding="utf-8") as f_r:
            for line in f_r:
                line = line.strip()
                intent_vocab.add(line)

        # Slot labels
        with open(os.path.join(split_dir, "seq.out"), "r", encoding="utf-8") as f_r:
            for line in f_r:
                line = line.strip()
                slots = line.split()
                for slot in slots:
                    slot_vocab.add(slot)

    # Write unique intent labels to intent_label.txt
    with open(os.path.join(data_dir, intent_label_vocab), "w", encoding="utf-8") as f_w:
        additional_tokens = ["UNK"]
        for token in additional_tokens:
            f_w.write(token + "\n")

        intent_vocab = sorted(intent_vocab)
        for intent in intent_vocab:
            f_w.write(intent + "\n")

    # Write unique slot labels to slot_label.txt
    with open(os.path.join(data_dir, slot_label_vocab), "w", encoding="utf-8") as f_w:
        additional_tokens = ["PAD", "UNK"]
        for token in additional_tokens:
            f_w.write(token + "\n")

        # Sort slot vocab based on the criteria you specified
        slot_vocab = sorted(slot_vocab, key=lambda x: (x[2:], x[:2]))
        for slot in slot_vocab:
            f_w.write(slot + "\n")

    print("Intent and slot vocabularies have been created successfully.")

if __name__ == "__main__":
    vocab_process("slu_data/syllable-level")
    print("Vocabulary processing completed.")
    # vocab_process("snips")
