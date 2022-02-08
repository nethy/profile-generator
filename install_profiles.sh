#!/usr/bin/env bash

set -e

PROFILES="configs/profiles.json"
TARGET="/d/raw_therapee_profiles"

python -m profile_generator $PROFILES

rm -rf $TARGET/*

mv profiles/* $TARGET
