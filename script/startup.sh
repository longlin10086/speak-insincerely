#!/usr/bin/env sh

echo "Please input your copilot api key: "
read -r API_KEY

docker build --tag speak-insincerely:v1 --build-arg USER_API_KEY="${API_KEY}" ..
docker run -d -p 7860:7860 -v /usr/src/speak-insincerely:/usr/src/app