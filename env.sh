#!/usr/bin/env sh

echo "Please input your copilot api key: "
read -r API_KEY
export OPENAI_API_KEY=${API_KEY}

