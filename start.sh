#!/bin/bash -x
PWD=`pwd`
activate () {
    . $PWD/venv/bin/activate
}

activate

#!/usr/bin/python3
python3 CountKeeper.py
