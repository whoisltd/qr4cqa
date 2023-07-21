# CUDA_VISIBLE_DEVICES=0 python src/train.py \
#     --model_name_or_path t5-small \
#     --text_column input \
#     --summary_column output \
#     --train_file data/en_train.csv \
#     --test_file data/en_test.csv \
#     --validation_file data/en_dev.csv \
#     --num_train_epochs 5 \
#     --do_train \
#     --do_eval \
#     --do_predict \
#     --save_steps 100 \
#     --evaluation_strategy steps \
#     --save_strategy no \
#     --eval_steps 100 \
#     --logging_steps 10 \
#     --weight_decay 0.01 \
#     --run_name wandb \
#     --output_dir weights/en-rewritting-t5-small \
#     --per_device_train_batch_size=8 \
#     --per_device_eval_batch_size=8 \
#     --save_total_limit 50 \
#     --overwrite_output_dir \
#     --predict_with_generate True \

CUDA_VISIBLE_DEVICES=0 python src/train.py \
    --model_name_or_path vinai/bartpho-syllable \
    --text_column input \
    --summary_column output \
    --train_file data/vi_train.csv \
    --test_file data/vi_test.csv \
    --validation_file data/vi_dev.csv \
    --num_train_epochs 5 \
    --do_train \
    --do_eval \
    --do_predict \
    --save_steps 100 \
    --evaluation_strategy steps \
    --save_strategy no \
    --eval_steps 100 \
    --logging_steps 10 \
    --weight_decay 0.01 \
    --run_name wandb \
    --output_dir weights/vi-rewritting-bartpho-syllable \
    --per_device_train_batch_size=8 \
    --per_device_eval_batch_size=8 \
    --save_total_limit 50 \
    --overwrite_output_dir \
    --predict_with_generate True \