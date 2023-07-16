#!/bin/sh
# We notice parameters:
# --model_name_or_path: addres
CUDA_VISIBLE_DEVICES=0 python src/train_kpg.py \
    --model_name_or_path weights/checkpoint-12000/optimizer.pt \
    --test_file data/test_btv_1.csv \
    --validation_file data/val.csv \
    --train_file data/train.csv \
    --do_predict \
    --output_dir weights/ \
    --predict_with_generate True

