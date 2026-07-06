#!/usr/bin/env bash

manual=1
auto=1
user_name=""

usage()
{
    echo "Usage: $0 <user name> [-a|--noauto] [-m|--nomanual]"
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -a|--noauto)
            auto=0
            shift
            ;;
        -m|--nomanual)
            manual=0
            shift
            ;;
        *)
            if [ -z "$user_name" ]; then
                user_name="$1"
            else
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

if [ -z "$user_name" ]; then
    usage
    exit 1
fi

mkdir -p ./user_backtag

query="user:$user_name -/c -/cr has:commentary"
echo " *** Starting commentary tagging session for user: $user_name"

if [ "$auto" == "1" ]; then
    echo " *** Running automatic first pass"
    ./commentary_downloader.py --tags "$query" ./user_backtag/$user_name.json || exit 1
    ./komentari.py --quiet --auto --file ./user_backtag/$user_name.json --output ./user_backtag/$user_name_s_auto.json || exit 1
    ./script_executer.py ./user_backtag/$user_name_s_auto.json || exit 1
fi

if [ "$manual" == "1" ]; then
    echo " *** Running manual mode"
    ./commentary_downloader.py --tags "$query" ./user_backtag/$user_name.json || exit 1
    ./komentari.py --file ./user_backtag/$user_name.json --output ./user_backtag/$user_name_s.json || exit 1
    ./script_executer.py ./user_backtag/$user_name_s.json || exit 1
fi

echo " *** Finished"
