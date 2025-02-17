#!/bin/bash

# Create ~/.bash_aliases if it doesn't exist
touch ~/.bash_aliases

# Ensure the file is writable
chmod 644 ~/.bash_aliases

# Overwrite ~/.bash_aliases with the desired aliases
cat > ~/.bash_aliases << 'EOF'
# File and Directory Navigation
alias ..='cd ..'                          # Go up one directory
alias ...='cd ../../..'                    # Go up three directories
alias ....='cd ../../../..'                # Go up four directories
alias ~='cd ~'                             # Go to home directory
alias dirs='dirs -v'                       # Show directory stack with line numbers

# Listing Files
alias ls='ls --color=auto -h'              # Colorized ls with human-readable sizes
alias ll='ls -la --color=auto -h'          # List all files, detailed
alias l.='ls -d .* --color=auto -h'        # List only hidden files
alias la='ls -A'                           # List all except . and ..
alias lsd='ls -d */'                       # List only directories

# File Operations (with Safety)
alias rm='rm -i'                           # Interactive remove
alias cp='cp -i'                           # Interactive copy
alias mv='mv -i'                           # Interactive move
alias mkdir='mkdir -p'                     # Create parent directories if they don't exist
alias touch='touch -c'                     # Don't create new files with touch

# File Viewing and Manipulation
alias cat='cat -vet'                       # Show non-printing characters in cat output
alias more='less'                          # Use less instead of more

# Searching and Grepping
alias grep='grep --color=auto -i'          # Colorize grep output, case-insensitive
alias egrep='egrep --color=auto'           # Same for egrep
alias fgrep='fgrep --color=auto'           # Same for fgrep

# Networking
alias ports='netstat -tulanp'              # Show open ports and their processes
alias ping='ping -c 5'                     # Ping with 5 packets (change as needed)
alias untar='tar -zxvf $1'                 # Untar files with the .tar.gz extension

# System Monitoring and Management
alias df='df -h'                           # Show disk usage in human-readable format
alias du='du -sh'                          # Show disk usage of the current directory
alias free='free -h'                       # Show memory usage in human-readable format
alias top='htop'                           # Use htop (install if needed) instead of top
alias ps='ps auxf'                         # Show all processes in a tree-like structure

# Miscellaneous
alias cls='clear'                          # Clear the terminal screen
alias h='history'                          # Show command history
alias history='history | nl'               # Show history with line numbers
alias hg='history | grep $1'               # Search using history command: $ hg somestring
alias j='jobs -l'                          # List background jobs

alias lol='echo "LOL!"'                    # Quick laugh

# Git Aliases
alias gs='git status'                      # Shorten git status to gs
alias ga='git add'                         # Shorten git add to ga
alias gd='git diff'                        # Shorten git diff to gd
alias gc='git commit'                      # Shorten git commit to gc

# Safeguards
alias rm='rm -I --preserve-root'           # Do not delete / or prompt if deleting more than 3 files at a time
alias mv='mv -i'                           # Interactive move
alias cp='cp -i'                           # Interactive copy
alias ln='ln -i'                           # Interactive symlink creation
alias chown='chown --preserve-root'        # Preserve root while changing ownership
alias chmod='chmod --preserve-root'        # Preserve root while changing permissions
alias chgrp='chgrp --preserve-root'        # Preserve root while changing group

# vi Aliases
alias vi='vim'                             # Use vim instead of vi
alias vis='vim "+set si"'                  # Open vim with 'smartindent' on

# Listener
alias listener='sudo rlwrap nc -lvnp 443'  # Create a netcat listener on port 443

# Wordlist Paths (common in security and penetration testing)
# export dirsmall='/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt'
# export dirmed='/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt'
# export rockyou='/usr/share/wordlists/rockyou.txt'
EOF

# Source the file to apply the aliases
source ~/.bash_aliases
