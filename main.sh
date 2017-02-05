#!/bin/bash
echo "NAMASTE"

sudo pip install beautifulsoup4
sudo pip install requests
sudo pip install pafy

export PAFY_BACKEND="internal"

python main.py
