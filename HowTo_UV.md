# Linux Ubuntu

curl -LsSf https://astral.sh/uv/install.sh | sh

#optional if you don't reboot
source $HOME/.local/bin/env 

uv venv .venv --python 3.13

source .venv/bin/activate

#libraries

uv pip install pympler