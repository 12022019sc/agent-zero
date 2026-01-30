#!/bin/bash

. "/ins/setup_venv.sh" "$@"
. "/ins/copy_A0.sh" "$@"

python /home/shayne/agent-zero/prepare.py --dockerized=true
# python /home/shayne/agent-zero/preload.py --dockerized=true # no need to run preload if it's done during container build

echo "Starting A0..."
exec python /home/shayne/agent-zero/run_ui.py \
    --dockerized=true \
    --port=80 \
    --host="0.0.0.0"
    # --code_exec_ssh_enabled=true \
    # --code_exec_ssh_addr="localhost" \
    # --code_exec_ssh_port=22 \
    # --code_exec_ssh_user="root" \
    # --code_exec_ssh_pass="toor"
