#!/usr/bin/env bash
apt update && apt upgrade -y && apt install python3 -y && pip3 install requests
echo ~/Softwarica-Gateway-AutoLogin/python3 main.py >> ~/.bashrc
