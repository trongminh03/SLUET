# BKAI Vietnamese SLU
## Overview
- This repo contain 2 module:
     - Speech to Text module.
     - Text Intent and Slot Filling module.
- Output of `Speech to Text module` will be feed in `Text Intent and Slot Filling module` to get the final prediction.
- P/s: Your device must have Docker and GPU. You should run it on Docker.
## Docker
- Build image by this command:
```
DOCKER_BUILDKIT=1 docker build -t slu .
```
- Then run the image by this command:
```
docker run -it --name docker_slu --gpus all --rm slu
```
## Speech to Text module
### Training
- We combine the ASR model and a LM model for higher Speech to Text accuracy.
- To train the ASR model:
    1. Go to SLU-ASR folder:
        ```
        cd SLU-ASR
        ```
    2. Generate data (optional):
        - You can use our generated wav data by download and unzip [this](https://drive.google.com/file/d/14F7XIRYTLqVzYr8nygXWPDTUazgzzhlg/view?usp=drive_link) and put it in the same folder as origin data and use the new [train_and_aug.jsonl file](https://drive.google.com/file/d/1Zkuuc4P74sVI1wpHMUw5PlBzpVdX95Rv/view?usp=sharing):
        - You can use gdown to download the file.
            - Generated wav data: 
                ```
                gdown 14F7XIRYTLqVzYr8nygXWPDTUazgzzhlg
                ```
            - train_and_aug.jsonl file: 
                ```
                gdown 1Zkuuc4P74sVI1wpHMUw5PlBzpVdX95Rv
                ```
    3. Prepare your dataset
        - To put your dataset in correct format and process it run: 
            ```
            bash prepare_train_data.sh [Path to wav data directory] [Path to jsonline train file]
            ```
        - Example :
            ```cmd
            bash prepare_train_data.sh /data/train_data/Train/ /data/train.jsonl
            ```
        - The processed data will be store in `txt_data/process_train.txt`
    4. Run
        - Start training from scratch:
            ```cmd
            python3 train.py -c config.toml
            ```
        - Change the number of workers, epochs, batch size, vv in `config.toml`
- To train LM model: 
    1. Go to the root folder of the repo. Train the LM model by:
        ```
        bash train_lm.sh [Path to origin jsonline train file]
        ```
        - Example:
        ```
        bash train_lm.sh /data/train.jsonl
        Note: Dont use the generated `train_and_aug.jsonl file` here.
        ```
        - The LM model will be stored in `your_ngram.binary`
- You can use our ASR model which trained on both generated data and original data and a LM model checkpoints through this link:
    - [ASR model](https://drive.google.com/file/d/1eUL7IgpPcofJeuLjf231cvBo2BSzRHJD/view?usp=sharing)
        ```
        gdown 1eUL7IgpPcofJeuLjf231cvBo2BSzRHJD
        ```
    - [LM model](https://drive.google.com/file/d/1XdQ0O-zyKEE8Z_glH9NZuj-Sj8v3jhkg/view?usp=drive_link)
        ```
        gdown 1XdQ0O-zyKEE8Z_glH9NZuj-Sj8v3jhkg
        ```
### Inference
```
bash inference.sh [Path to your wav test file lists] [Path to model.tar] [Path to LM model]
```
    
- Example:
```
bash inference.sh /data/public_test/ best_model.tar your_3gram.binary
```
- Then the final transcript be in `process_trans_file.txt`
## Text Intent and Slot Filling module
### Training 
1. Prepare your data
    - Run the following command to pre-process train.jsonl and prepare data for training:
        ```
        python3 slu_data_1/data_process.py -j [Path to train.jsonl file]
        ```
    - Example :
        ```cmd
        python3 slu_data_1/data_process.py -j /data/train.jsonl
        ```
    The processed data will be stored in `slu_data_1/syllable-level`
2. Run 
    - Run the following bash file to start training: 
        ```cmd
        ./run_jointIDSF_PhoBERTencoder.sh
        ```
### Inference
- Here is [model checkpoints link](https://drive.google.com/drive/folders/1tZ-508QnyfQEh1_xzkoVjwkSkW38I04f?usp=drive_link) in case you want to make inference without training the models from scratch
- Then run this command for inference:
```
 bash inference_JointIDSF.sh [Path to output transcript of ASR module] [Path to model checkpoints] [saved name]
```
- Example:
```
bash inference_JointIDSF.sh SLU-ASR/process_trans_file.txt JointIDSF_PhoBERTencoder_SLU/4e5/0.15/100 predictions.jsonl 
```
- Then the final output will be automatically zipped as `Submission.zip`.