#!/bin/bash

echo "$(echo $(timew | grep 'Tracking')) | $(echo $(timew | grep 'Total')) | $(echo $(timew day | grep 'Tracked'))"
