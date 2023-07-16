# Impliment Question Rewriting for Conversational Question Answering

[VietAI Reseach]

Impliment Question Rewriting for Conversational Question Answering 

# Installation

## Install Pytorch + CUDA Toolkit
Install Pytorch in this [link](https://pytorch.org/get-started/previous-versions/) compatible with your CUDA.
```bash
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
```

## Option 1: Install libraries

```bash
pip install -r requirements.txt
```

Update submodules if it needs.
```bash
bash init.sh
```

## Option 2: Install step-by-step

### Install libraries

```bash
pip install underthesea seqeval datasets sentencepiece
```

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

Change configuration in src/bin/train.sh

```bash
bash src/bin/train.sh
```