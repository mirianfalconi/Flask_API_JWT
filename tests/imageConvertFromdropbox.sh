#!/bin/bash

echo "Unit Tests:  /image/convert/fromdropbox
"

token=$(python3.7 generate_jwt.py)

echo 'URL to dropbox image:   #Like: "/sheetgo/_tmp_image.png"'
read url

curl=$(curl -s http://127.0.0.1:5000/image/convert/fromdropbox -F url="$url" -H  $token >> dropboximage)
echo "from dropbox PNG >> JPG or JPG >> PNG"
echo "dropboximage in tests folder
"

curl=$(curl -s http://127.0.0.1:5000/image/convert/fromdropbox -F url="$url")
echo "without a token"
echo $curl
echo ""

curl=$(curl -s http://127.0.0.1:5000/image/convert/fromdropbox -F url=@mil.xlsx -H  $token)
echo "wrong extension"
echo $curl
echo ""


curl=$(curl -s http://127.0.0.1:5000/image/convert/fromdropbox -F url= -H  $token)
echo "No url"
echo $curl
echo ""

curl=$(curl -s http://127.0.0.1:5000/image/convert/fromdropbox -F url="" -H  $token)
echo "wrong url"
echo $curl
echo ""


curl=$(curl -s http://127.0.0.1:5000/image/convert/fromdropbox -H  $token)
echo "GET request"
echo $curl
echo ""
