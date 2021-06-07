#!/usr/bin/env bash

arduino-cli compile --fqbn arduino:avr:nano firmware/
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:nano firmware/