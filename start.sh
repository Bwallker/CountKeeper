#!/bin/bash -x
PWD=`pwd`
activate () {
    source $PWD/CountKeeperVenv/bin/activate
}

activate

#!/usr/bin/python3
python3 CountKeeper.py
