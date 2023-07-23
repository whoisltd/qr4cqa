## Preprocess data to suitable Vietnamese language format

### Translate
By using googletrans API. The following examples will run on example datasets to translate from any language to Vietnamese. You can do it by run the command.
```
python3 src/data_utils/optimize_trans_CANARD.py \
    --file_text "dev.json" \
    --file_name_save "dev_vi.json" 
```
or use file .sh
```
bash src/data_utils/optimize_trans_CANARD.py
```

