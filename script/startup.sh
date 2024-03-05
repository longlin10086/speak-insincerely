#!/usr/bin/env sh

echo "Please input your copilot api key: "
read -r API_KEY


echo "---------------------start to build-----------------------------"
docker build --tag speak-insincerely:v1 .
echo "---------------------building finished-----------------------------"
docker run -d -p 7860:7860 -e OPENAI_API_KEY="${API_KEY}" speak-insincerely:v1