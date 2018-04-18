#!/bin/bash

# Contents copied from https://circleci.com/docs/2.0/project-walkthrough/#deploying-to-heroku,
# with the only change being the URL to the myob-webapi GitHub repository
git remote add heroku https://github.com/ktenedios/myob-webapi.git
wget https://cli-assets.heroku.com/branches/stable/heroku-linux-amd64.tar.gz
sudo mkdir -p /usr/local/lib /usr/local/bin
sudo tar -xvzf heroku-linux-amd64.tar.gz -C /usr/local/lib
sudo ln -s /usr/local/lib/heroku/bin/heroku /usr/local/bin/heroku

cat > ~/.netrc << EOF
machine api.heroku.com
  login $HEROKU_LOGIN
  password $HEROKU_API_KEY
machine git.heroku.com
  login $HEROKU_LOGIN
  password $HEROKU_API_KEY
EOF

# Add heroku.com to the list of known hosts
ssh-keyscan -H heroku.com >> ~/.ssh/known_hosts
