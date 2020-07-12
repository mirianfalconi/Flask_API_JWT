#!/bin/bash

echo "Unit Tests:  /excel/info
"

token=$(python3.7 generate_jwt.py)
curl=$(curl -s http://127.0.0.1:5000/excel/info -F file=@mil.xlsx -H $token )
echo "Tabs from the excel file ordered alphabetically"
echo $curl
echo ""

curl=$(curl -s http://127.0.0.1:5000/excel/info -F file=@mil.xlsx)
echo "without a token"
echo $curl
echo ""


curl=$(curl -s http://127.0.0.1:5000/excel/info -F file= -H  $token)
echo "blank file arg"
echo $curl
echo ""


curl=$(curl -s http://127.0.0.1:5000/excel/info -F file="aa" -H  $token)
echo "wrong path file"
echo $curl
echo ""


curl=$(curl -s http://127.0.0.1:5000/excel/info -F file=@read.me -H $token )
echo "wrong extension"
echo $curl
echo ""

curl=$(curl -s http://127.0.0.1:5000/excel/info -H $token )
echo "GET request"
echo $curl
echo ""
