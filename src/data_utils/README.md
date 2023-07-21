## Preprocess data to suitable Vietnamese language format

### Translate

By using googletrans API. The following examples will run on example datasets to translate from any language to Vietnamese.

```
python3 optimize_trans_CANARD.py \
    --file_text "dev.json" \
    --file_name_save "dev_vi.json"
```
