#!/bin/bash                                                                     
git submodule sync
git submodule update --init --recursive
echo "Done sync"

git pull && git submodule update
echo "Pull and update submodule: Done "