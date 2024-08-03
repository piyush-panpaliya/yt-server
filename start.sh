#!/bin/bash

service nscd start
exec python3 app.py