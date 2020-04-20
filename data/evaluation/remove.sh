#!/bin/bash

# Run this to remove extraneous files

rm -rf __pycache__

rm cacm/querytemp
rm cacm/reltemp
rm -rf cacm/__pycache__

rm cisi/querytemp
rm cisi/reltemp
rm -rf cisi/__pycache__

rm med/querytemp
rm med/reltemp
rm -rf med/__pycache__

rm time/querytemp
rm time/reltemp
rm -rf time/__pycache__