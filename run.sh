#!/usr/bin/env bash

# the run script for running the fraud detection algorithm with a python file, antifraud.py

# I'll execute my programs, with the input directory paymo_input and output the files in the directory paymo_output


python ./src/antifraud.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_input/batch_payment_fixed.csv ./paymo_input/stream_payment_fixed.csv ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt
