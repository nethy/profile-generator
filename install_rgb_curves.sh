#!/usr/bin/env bash

set -e

PROFILES="configs/color_grading.json"
TARGET="/d/pictures/raw/_rt_profiles"

python -m profile_generator.tools.rgb_curves $PROFILES

mv profiles/* $TARGET
