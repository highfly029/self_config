# 在 Mac OS 中，通过 brew 安装
brew install tmux

# 安装Oh My Tmux
git clone https://github.com/gpakosz/.tmux.git ~/.tmux
ln -s -f ~/.tmux/.tmux.conf ~/.tmux.conf
cp ~/.tmux/.tmux.conf.local ~/


# 修改.tmux.conf.local配置
#切换鼠标
set -g mouse on 

#开启vi模式
set -g status-keys vi
set -g mode-keys vi
设置->General->Selection->Applications in terminal may access clipboard

#能够正常访问系统剪贴板 已经默认支持了
#set-option -g default-command "reattach-to-user-namespace -l zsh"

#增大缓存
set-option -g buffer-limit 100000

# tmux的插件管理tpm
https://github.com/tmux-plugins/tpm