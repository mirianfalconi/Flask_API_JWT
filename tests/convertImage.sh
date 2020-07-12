#!/bin/bash

echo "Unit Tests:  /image/convert 
"

token=$(python3.7 generate_jwt.py)

curl=$(curl -s http://127.0.0.1:5000/image/convert -F file=@rocket.png -H  $token >> output1)
echo "PNG >> JPG"
echo "rocket.png >> output1 in tests folder
"

curl=$(curl -s http://127.0.0.1:5000/image/convert -F file=@rocket.jpg -H  $token >> output2)
echo "JPG >> PNG"
echo "rocket.jpg >> output2 in tests folder
"

curl=$(curl -s http://127.0.0.1:5000/image/convert -F file=@rocket.png)
echo "without a token"
echo $curl
echo ""

curl=$(curl -s http://127.0.0.1:5000/image/convert -F file=@mil.xlsx -H  $token)
echo "wrong extension"
echo $curl
echo ""

curl=$(curl -s http://127.0.0.1:5000/image/convert -F file= -H  $token)
echo "No file"
echo $curl
echo ""

curl=$(curl -s http://127.0.0.1:5000/image/convert -F file="sd" -H  $token)
echo "wrong name"
echo $curl
echo ""


curl=$(curl -s http://127.0.0.1:5000/image/convert -H $token )
echo "GET request"
echo $curl
echo ""
