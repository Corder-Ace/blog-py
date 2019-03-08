#!/bin/bash
. /etc/profile
export PATH=/usr/local/bin:$PATH

_p=/home/backend/blog-py
_l=/home/moyun/log

_start(){
    if [ ! -d $_l ];then
        mkdir $_l
    fi
    cd $_p
    nohup python3 run.py >> $_l/views.log 2>&1 &
}

count=`pgrep -f 'python3 run.py' | wc -l`
if [ $count -eq 0 ];then
    _start
fi
