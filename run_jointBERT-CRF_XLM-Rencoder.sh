export lr=4e-5
export c=0.45
export s=10
echo "${lr}"
export MODEL_DIR=JointBERT-CRF_XLM-Rencoder_SLU_augmented
export MODEL_DIR=$MODEL_DIR"/"$lr"/"$c"/"$s
echo "${MODEL_DIR}"
python3 main.py --token_level syllable-level \
                  --model_type xlmr \
                  --model_dir $MODEL_DIR \
                  --data_dir slu_data_1 \
                  --seed $s \
                  --do_train \
                  --do_eval \
                  --save_steps 140 \
                  --logging_steps 140 \
                  --num_train_epochs 50 \
                  --tuning_metric mean_intent_slot \
                  --use_crf \
                  --gpu_id 0 \
                  --embedding_type soft \
                  --intent_loss_coef $c \
                  --learning_rate $lr