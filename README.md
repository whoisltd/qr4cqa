# Impliment Question Rewriting for Conversational Question Answering

[VietAI Reseach]

Impliment Question Rewriting for Conversational Question Answering 

# Install Pytorch + CUDAToolkit
Install Pytorch in this [link](https://pytorch.org/get-started/previous-versions/) compatible with your CUDA.
```bash
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
```

```bash
pip install underthesea seqeval datasets sentencepiece
```

# Install libraries

```bash
git clone https://github.com/huggingface/transformers --branch v4.27.0 --single-branch
cd transformers
pip install -e .
```

# Process data

```bash
python process_data.py
```

# Training

Change configuration in bin/train\_kpg.sh

```bash
bash bin/train_kpg.sh
```