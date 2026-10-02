#!/bin/sh

./commentary_downloader.py --tags "-commentary -commentary_request" full_auto_pass.json
./komentari.py --auto --file full_auto_pass.json --output full_auto_pass_s.json --quiet
./script_executor.py full_auto_pass_s.json
