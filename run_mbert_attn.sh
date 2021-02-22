lr_list=(1e-5 2e-5 3e-5 4e-5 5e-5)
for lr in "${lr_list[@]}" 
do
echo "${lr}"
export MODEL_DIR=viatis_mbert_attn_200
export MODEL_DIR=$MODEL_DIR"/"$lr
echo "${MODEL_DIR}"
/usr/bin/python3.7 main.py --task vi-atis-fix \
                  --model_type mbert \
                  --model_dir $MODEL_DIR \
                  --data_dir data \
                  --seed 1 \
                  --do_train \
                  --do_eval \
                  --save_steps 140 \
                  --logging_steps 140 \
                  --num_train_epochs 1000 \
                  --tuning_metric mean_intent_slot \
                  --use_intent_context_attention \
                  --attention_embedding_size 200 \
                  --gpu_id 1 \
                  --learning_rate $lr
done