#!/bin/bash
RELDIR=../


SCRIPT=`readlink -f $0`
SCRIPTPATH=`dirname $SCRIPT`
echo "[0] Script Directory: $SCRIPTPATH"
REDHAWK=`readlink -f $SCRIPTPATH/$RELDIR`
echo "[1] Adding $REDHAWK to path."

export PYTHONPATH="$REDHAWK:$PYTHONPATH"
echo "[2] New Python Path is $PYTHONPATH"

echo "[3] Starting bash"
echo "[4] Run nosetests from the $REDHAWK directory."

bash --norc --noprofile

