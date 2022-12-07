#!/bin/bash

fly scale count 0
fly deploy --local-only
fly scale count 1
