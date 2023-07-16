#!/bin/sh
# We notice parameters:
# --model_name_or_path: model's address in hugging face. We can try "vinai/bartpho-syllable", "google/mt5-base", ...
# --train_file / test_file / validation_file: address of train/test/validation
# --output_dir: address to save model
# CUDA_VISIBLE_DEVICES=1 python src/train_kpg.py \
#     --model_name_or_path vinai/bartpho-syllable \
#     --train_file data/train.csv \
#     --test_file data/test.csv \
#     --validation_file data/val.csv \
#     --num_train_epochs 10 \
#     --do_train \
#     --do_eval \
#     --do_predict \
#     --save_steps 2000 \
#     --logging_steps 2000 \
#     --run_name wandb \
#     --output_dir weights_bartpho/ \
#     --per_device_train_batch_size=1 \
#     --per_device_eval_batch_size=1 \
#     --save_total_limit 50 \
#     --overwrite_output_dir \
#     --predict_with_generate True

# VietAI/vit5-base 
# CUDA_VISIBLE_DEVICES=1 python src/train_kpg.py \
#     --model_name_or_path VietAI/vit5-base \
#     --text_column content \
#     --summary_column kw \
#     --train_file data/train.csv \
#     --test_file data/test.csv \
#     --validation_file data/test.csv \
#     --num_train_epochs 20 \
#     --do_train \
#     --do_eval \
#     --do_predict \
#     --save_steps 1000 \
#     --logging_steps 1000 \
#     --run_name wandb \
#     --output_dir weights_vit5_20epochs/ \
#     --per_device_train_batch_size=1 \
#     --per_device_eval_batch_size=1 \
#     --save_total_limit 50 \
#     --overwrite_output_dir \
#     --predict_with_generate True

# VietAI/vit5-base vietnews
# CUDA_VISIBLE_DEVICES=1 python src/train_kpg.py \
#     --model_name_or_path VietAI/vit5-base-vietnews-summarization \
#     --text_column CustomerAddress \
#     --summary_column areaFull \
#     --train_file data/train.csv \
#     --test_file data/test.csv \
#     --validation_file data/test.csv \
#     --num_train_epochs 5 \
#     --do_train \
#     --do_eval \
#     --do_predict \
#     --save_steps 100 \
#     --evaluation_strategy steps \
#     --save_strategy no \
#     --eval_steps 100 \
#     --logging_steps 100 \
#     --weight_decay 0.01 \
#     --run_name wandb \
#     --output_dir weights/address \
#     --per_device_train_batch_size=16 \
#     --per_device_eval_batch_size=1 \
#     --save_total_limit 50 \
#     --overwrite_output_dir \
#     --predict_with_generate True \

# CUDA_VISIBLE_DEVICES=1 python src/train_kpg.py \
#     --model_name_or_path VietAI/vit5-base-vietnews-summarization \
#     --text_column CustomerAddress \
#     --summary_column areaFull \
#     --train_file data/train_v1.csv \
#     --test_file data/test_v1.csv \
#     --validation_file data/test_v1.csv \
#     --num_train_epochs 5 \
#     --do_train \
#     --do_eval \
#     --do_predict \
#     --save_steps 1000 \
#     --evaluation_strategy steps \
#     --save_strategy no \
#     --eval_steps 1000 \
#     --logging_steps 100 \
#     --weight_decay 0.01 \
#     --run_name wandb \
#     --output_dir weights/address_v1_vit5_base \
#     --per_device_train_batch_size=16 \
#     --per_device_eval_batch_size=8 \
#     --save_total_limit 50 \
#     --overwrite_output_dir \
#     --predict_with_generate True \
#     --fp16

CUDA_VISIBLE_DEVICES=0 python src/train_kpg.py \
    --model_name_or_path google/mt5-small \
    --text_column CustomerAddress \
    --summary_column areaFull \
    --train_file data/train_v1.csv \
    --test_file data/test_v1.csv \
    --validation_file data/test_v1.csv \
    --num_train_epochs 5 \
    --do_train \
    --do_eval \
    --do_predict \
    --save_steps 1000 \
    --evaluation_strategy steps \
    --save_strategy no \
    --eval_steps 1000 \
    --logging_steps 100 \
    --weight_decay 0.01 \
    --run_name wandb \
    --output_dir weights/address_v1_vit5_small \
    --per_device_train_batch_size=16 \
    --per_device_eval_batch_size=16 \
    --save_total_limit 50 \
    --overwrite_output_dir \
    --predict_with_generate True \