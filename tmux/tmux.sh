#!/bin/bash

tmux has-session -t local
if [ $? != 0 ]
then
  tmux new-session -s local -n self -d

  tmux neww -n test -t local -d

  tmux neww -n workConfig -t local -d
  tmux select-window -t local:3
  tmux send-keys "cd /Users/admin/www/ss/ss-data-config/gamedata" C-m
  tmux split-window -v -t workConfig
  tmux select-window -t local:3.1
  tmux send-keys "cd /Users/admin/www/ss/ss-config" C-m  

  tmux neww -n workSpace -t local -d
  tmux select-window -t local:4
  tmux send-keys "cd /Users/admin/www/ss/ss-server" C-m
  tmux split-window -v -t workSpace
  tmux select-window -t local:4.1
  tmux send-keys "cd /Users/admin/www/ss/logs" C-m  

  tmux new-session -s issue -n deploy -d
  tmux neww -n game1 -t issue -d
  tmux neww -n game2 -t issue -d
fi
tmux attach -t local

