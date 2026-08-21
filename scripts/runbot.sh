#!/usr/bin/env bash

./komentari.py --query "-commentary -commentary_request has:commentary age:>5min" --auto --quiet --same-page "$@"
