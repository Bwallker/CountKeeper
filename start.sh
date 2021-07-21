#!/bin/bash
PWD=`pwd`
activate () {
    source $PWD/count_keeper_venv/bin/activate
}

activate

#!/usr/bin/python3
python3 count_keeper.py
