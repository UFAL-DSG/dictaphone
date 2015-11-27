#!/usr/bin/env bash

LANG=$1
TMP=$2

STAGE=1

PYTHON=python2.7
SEQUITUR=./tools/sequitur-g2p/bin/g2p.py
SEQUITUR_PATH=./tools/sequitur-g2p/lib/python2.7/site-packages
ASCII_IPA_PATH=./tools/ascii-ipa
mkdir -p $TMP

cat $LANG/*.dict > $TMP/all.dict

PYTHONPATH=$ASCII_IPA_PATH:$PYTHONPATH ./src/clean_dict.py $TMP/all.dict $TMP/all.clean.dict || exit 1


DICT_CLEAN=$TMP/all.clean.dict

MODEL_1=$TMP/model-1

if [ $STAGE -le 3 ]; then
  echo "Training first-order G2P model (log in '$TMP/model-1.log') ..."
  PYTHONPATH=$SEQUITUR_PATH:$PYTHONPATH $PYTHON $SEQUITUR \
    --train $DICT_CLEAN --devel 5% --write-model $MODEL_1 >$TMP/model-1.log 2>&1 || exit 1
fi

MODEL_2=$TMP/model-2

if [ $STAGE -le 4 ]; then
  echo "Training second-order G2P model (log in '$TMP/model-2.log') ..."
  PYTHONPATH=$SEQUITUR_PATH:$PYTHONPATH $PYTHON $SEQUITUR \
    --model $MODEL_1 --ramp-up --train $DICT_CLEAN \
    --devel 5% --write-model $MODEL_2 \
    >$TMP/model-2.log 2>&1 || exit 1
fi

MODEL_3=$TMP/model-3

if [ $STAGE -le 5 ]; then
  echo "Training third-order G2P model (log in '$TMP/model-3.log') ..."
  PYTHONPATH=$SEQUITUR_PATH:$PYTHONPATH $PYTHON $SEQUITUR \
    --model $MODEL_2 --ramp-up --train $DICT_CLEAN \
    --devel 5% --write-model $MODEL_3 \
    >$TMP/model-3.log 2>&1 || exit 1
fi

MODEL_4=$TMP/model-4

if [ $STAGE -le 4 ]; then
  echo "Training fourth-order G2P model (log in '$TMP/model-4.log') ..."
  PYTHONPATH=$SEQUITUR_PATH:$PYTHONPATH $PYTHON $SEQUITUR \
    --model $MODEL_3 --ramp-up --train $DICT_CLEAN \
    --devel 5% --write-model $MODEL_4 \
    >$TMP/model-4.log 2>&1 || exit 1
fi

MODEL_5=$TMP/model-5

if [ $STAGE -le 5 ]; then
  echo "Training fifth-order G2P model (log in '$TMP/model-5.log') ..."
  PYTHONPATH=$SEQUITUR_PATH:$PYTHONPATH $PYTHON $SEQUITUR \
    --model $MODEL_4 --ramp-up --train $DICT_CLEAN \
    --devel 5% --write-model $MODEL_5 \
    >$TMP/model-5.log 2>&1 || exit 1
fi

cp $MODEL_5 $LANG/g2p.model

echo "G2P training finished OK!"
exit 0
