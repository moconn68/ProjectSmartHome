#!/bin/sh
node --max_old_space_size=512 $(which npm) install $1
