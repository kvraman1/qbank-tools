#!/bin/bash

cur_dir=`dirname $0`
source "$cur_dir/deploy-common.sh"


cp -r "$cur_dir/../dashboard" "$DEPLOY_ROOT/"
cp -r "$cur_dir/../helpers" "$DEPLOY_ROOT/"
cp -r "$cur_dir/../siman" "$DEPLOY_ROOT/"
cp -r "$cur_dir/../utilities" "$DEPLOY_ROOT/"
cp $cur_dir/../deploy/* "$DEPLOY_ROOT/"
cp $cur_dir/../requirements.txt "$DEPLOY_ROOT/"


remote=""
if [[ $1 == 'main' || -z "$1" ]]
then
    cp "$cur_dir/Procfile_main_app" "$DEPLOY_ROOT/Procfile"
    remote=$QBANK_MAIN
elif [[ $1 == 'sim-eval' ]]
then
    cp "$cur_dir/Procfile_sim_eval_app" "$DEPLOY_ROOT/Procfile"
    remote=$QBANK_SIM_EVAL
fi


cd $DEPLOY_ROOT

git add -A
dt=`date +"%Y-%m-%d_%H-%M"`
git commit -m "$dt"

if [[ $2 == 'local' ]]
then
    heroku local
else
    echo "deploying $remote"
    git push $remote master
    heroku open -a $remote
fi



