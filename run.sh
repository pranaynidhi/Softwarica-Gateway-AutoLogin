#!/usr/bin/env bash
apt update && apt upgrade -y && apt install python3 && pip3 install requests
echo python3 main.py >> ~/.bashrc
