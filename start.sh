#!/bin/bash -x
PWD=`pwd`
activate () {
    . $PWD/CountKeeperVenv/bin/activate
}

activate

#!/usr/bin/python3
python3 CountKeeper.py
