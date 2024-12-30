# SLUET: A novel method for Vietnamese Spoken Language Understanding
## Overview
- This repository contains 2 modules:
     - Speech to Text module.
     - Text Intent and Slot Filling module.
- Output of `Speech to Text module` will be fed into `Text Intent and Slot Filling module` to get the final prediction.
- P/s: Your device must have Docker and GPU. You should run it on Docker.
- You first need to clone the repository including its submodules:
    ```
    git clone --recurse-submodules https://github.com/trongminh03/SLUET.git
    ```

## Dataset
- SLUET is trained and evaluated on VN-SLU dataset. Please refer to the below links: 
    - Audio files: https://drive.google.com/drive/folders/1QJFQjwNl4tmlf4R1yt4W3gfUzsiF-kWp
    - Dataset labels: https://drive.google.com/drive/folders/1BDKK8vg-tByTY2EUWi6aYDjqG1NIFG8H
The final directory structure will be as follows:
```bash
Vietname_SLU_data
|
├─ data_interspeech
|   ├── train
|   |     ├── 64b420ff8e16f5f56e45a2b7.wav
|   |     ├── 64b420118e16f55e6945a2a5.wav
|   |     ├── ...
|   |
|   ├── dev
|   |     ├── 64a82d17a35d0a0764e9c1ea.wav
|   |     ├── 659438782883f803e891bfbd.wav
|   |     ├── ...
|   |  
|   └── test
|   |     ├── 64a2d963f5f4465ad1799206.wav
|   |     ├── 64b3fea5d6657a2b648ce03a.wav
|   |     ├── ...
|     
└── metadata_slu
    ├── train.jsonl
    ├── dev.jsonl
    └── test.jsonl
    
```
## Docker
- Build image using this command:
```
DOCKER_BUILDKIT=1 docker build -t sluet .
```
- Then run the image using this command:
```
docker run -it --name docker_sluet --gpus all --rm sluet
```
## Speech to Text module
### Training
- We combine the ASR model with a LM model for higher Speech to Text accuracy.
- To train the ASR model:
    1. Go to SLU-ASR folder:
        ```
        cd SLU-ASR
    2. Prepare your dataset
        - To put your dataset in correct format and process it run: 
            ```
            bash prepare_train_data.sh [Path to wav data directory] [Path to jsonline train file]
            ```
        - Example :
            ```cmd
            bash prepare_train_data.sh /data/train_data/Train/ /data/train.jsonl
            ```
        - The processed data will be store in `txt_data/process_train.txt`
    5. Run
        - Start training from scratch:
            ```cmd
            python3 train.py -c config.toml
            ```
        - Change the number of workers, epochs, batch size, vv in `config.toml`
        - The model will be stored in `saved/ASR/checkpoints/best_model.tar`. If you train more than one model, the newer checkpoints will replace the older. 
- To train LM model: 
    1. Go to the root folder of the repository. Train the LM model by:
        ```
        bash train_lm.sh [Path to origin jsonline train file]
        ```
        - Example:
        ```
        bash train_lm.sh /data/train.jsonl
        ```
        - The LM model will be stored in `your_ngram.binary`
<!-- - You can use our ASR model checkpoints and a LM model checkpoints through this link:
    - [First ASR model](https://drive.google.com/drive/folders/1eXHr0Q4RvhQTIghBY3gL3Lm2CoH3zbgf?usp=drive_link)
        ```
        gdown --folder 1eXHr0Q4RvhQTIghBY3gL3Lm2CoH3zbgf
        ``` 
    - [Second ASR model](https://drive.google.com/drive/folders/1SE3kA912bTMZohwb04iZ6dn_RHl94yoL?usp=sharing)
        ```
        gdown --folder 1SE3kA912bTMZohwb04iZ6dn_RHl94yoL
        ```
    - [LM model](https://drive.google.com/file/d/1XdQ0O-zyKEE8Z_glH9NZuj-Sj8v3jhkg/view?usp=sharing)
        ```
        gdown 1XdQ0O-zyKEE8Z_glH9NZuj-Sj8v3jhkg
        ``` -->
### Inference
- First, go to SLU-ASR folder then run
```
bash inference.sh  [Path to your wav test file lists] [Path to LM model] [save_path]
```
    
- Example:
```
bash inference.sh /data/public_test/ 3_ngram.binary process_trans_file.txt
```

## Text Intent and Slot Filling module
### Training 
1. Prepare your data
    - Run the following command to pre-process default `train.jsonl` file and prepare data for training:
        ```
        python3 slu_data/data_process.py -m [Path to metadata jsonl files]
        ```
    The processed data will be stored in `slu_data/syllable-level`
2. Run 
    - Run the following bash file to start training: 
        ```cmd
        ./run_jointIDSF_PhoBERTencoder.sh
        ```
### Inference
Run this command for inference: 
```
bash inference_JointIDSF.sh [Path to output transcript of ASR module] [Path to model checkpoints] [saved name]
```
- Example:
```
bash inference_JointIDSF.sh SLU-ASR/final_trans.txt JointIDSF_PhoBERTencoder_SLU/4e5/0.15/100 predictions.jsonl 
```

### Ensemble model inference
- For higher accuracy we apply confidence score ensemble method.
- Edit ``` model_list.txt ``` file which includes multiple model names and weights that you want to ensemble. 
- Then run:
```
bash inference_ensemble.sh [Path to transcript file]
```
