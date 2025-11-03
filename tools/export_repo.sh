#!/bin/bash
# usage: ./tools/export_repo.sh ToySoldiers_complete new-repo-name
set -e
DIR=$1
REPO=$2
cd "$DIR"
git init
git remote add origin "git@github.com:Immutablemike/$REPO.git"
git add .
git commit -m "Initial import from factory"
git push -u origin main