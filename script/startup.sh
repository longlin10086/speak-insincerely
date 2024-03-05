#!/usr/bin/env sh

echo "Please input your copilot api key: "
read -r API_KEY


echo "---------------------start to build-----------------------------"
docker build --tag speak-insincerely:v1 --build-arg USER_API_KEY="${API_KEY}" .
echo "---------------------building finished-----------------------------"
docker run -d -p 7860:7860 speak-insincerely:v1