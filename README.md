# YOLOv6 - VAIPE baseline
## Introduction

YOLOv6 is a single-stage object detection framework dedicated to industrial applications, with hardware-friendly efficient design and high performance.
This repo is inherited from official implementation repo of Yolov6 with modifications in evaluation (wmAP) and convert dataset for AI4VN challenge.
With yolov6s configuration, this baseline achieved approximately 44% wmAP on public test. Feel free to fork and edit this baseline. You should utilize the logical constraints from Prescription data by adding OCR module in this repo.


## Quick Start

### Install

```shell
git clone https://github.com/meituan/YOLOv6
cd YOLOv6
pip install -r requirements.txt
```

### Training

Single GPU

```shell
python tools/train.py --batch 32 --conf configs/yolov6s.py --data data/coco.yaml --device 0
                                        configs/yolov6n.py
```

Multi GPUs (DDP mode recommended)

```shell
python -m torch.distributed.launch --nproc_per_node 8 tools/train.py --batch 256 --conf configs/yolov6s.py --data data/coco.yaml --device 0,1,2,3,4,5,6,7
                                                                                        configs/yolov6n.py
```

- conf: select config file to specify network/optimizer/hyperparameters
- data: prepare [COCO](http://cocodataset.org) dataset, [YOLO format coco labes](https://github.com/meituan/YOLOv6/releases/download/0.1.0/coco2017labels.zip) and specify dataset paths in data/ai4vn.yaml.
Your dataset can be created by running 
```shell
python data/convert_ai4vn.py
```

to convert unzipped folder to coco format labels
To run this file successfully, you might be replace the path '/home/ubuntu/shared/' with your own unzipped path. Notes that
all the folders like public test, public train should be located together in your path like '/home/ubuntu/shared/public_test/'. The structure of ai4vn folder should be 
```
data/
    ├──ai4vn/
        ├── annotations
        |    "will be created by Yolov6, you don't need to create it manually"
        ├──images
        |    ├──train
        |    ├──val
        |    ├──test
        ├──labels
            ├──train
            ├──val
            ├──test

```
### Evaluation

Run evaluation on VAIPE public test

```shell
python tools/eval.py --data data/ai4vn.yaml --batch 32 --weights yolov6s.pt --task val
                                                                yolov6n.pt
```

### Resume
If your training process is corrupted, you can resume training by
```
# single GPU traning.
python tools/train.py --resume
# multi GPU training.
python -m torch.distributed.launch --nproc_per_node 8 tools/train.py --resume
```
Your can also specify a checkpoint path to `--resume` parameter by
```
# remember replace /path/to/your/checkpoint/path to the checkpoint path which you want to resume training.
--resume /path/to/your/checkpoint/path

```
