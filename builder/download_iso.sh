#!/bin/bash

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

source "$PROJECT_ROOT/configs/ubuntu.conf"

ISO_DIR="$PROJECT_ROOT/downloads"

mkdir -p "$ISO_DIR"

BASE_URL="https://releases.ubuntu.com/${UBUNTU_RELEASE}/"
