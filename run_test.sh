rm data/cache*
/usr/bin/python3.7 main.py --task vi-atis-fix \
                  --model_type mbert \
                  --model_dir test_run \
                  --data_dir data \
                  --do_train \
                  --do_eval \
                  --seed 1 \
                  --tuning_metric mean_intent_slot \
                  --save_steps 140 \
                  --logging_steps 140 \
                  --num_train_epochs 1000 \
                  --use_intent_context_concat \
                  --intent_embedding_size 300 \
                  --use_crf \
                  --embedding_type soft \
                  --intent_loss_coef 0.5 \
                  --early_stopping 10 \
                  --learning_rate 3e-5 