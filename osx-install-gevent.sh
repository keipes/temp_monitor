#!/usr/bin/env sh

echo "You may need to update the exact paths to libevent"
sudo CFLAGS="-I /usr/local/Cellar/libevent/2.0.22/include -L /usr/local/Cellar/libevent/2.0.22/lib -std=c99" pip install gevent

