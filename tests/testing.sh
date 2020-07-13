
#!/bin/bash

token=$(python3.7 generate_jwt.py)
#
# LOCAL_HOST = 'http://127.0.0.1:5000'
# DROPBOX_FOLDER = '/sheetgo/_tmp_image.png'

echo "This script receives the parameters via terminal and bypass them to the API

"


read -p "Enter local_host [http://127.0.0.1:5000]: " LOCAL_HOST
LOCAL_HOST=${LOCAL_HOST:-http://127.0.0.1:5000}
echo $LOCAL_HOST
echo



PS3='Please choose a endpoint: '
options=("/excel/info" "/image/convert" "/image/convert/fromdropbox" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "/excel/info")
              read -p "Enter a excel file (.xlsx) to order tabs alphabetically [mil.xlsx]:" file
              file=${file:-mil.xlsx}
              curl=$(curl -s "$LOCAL_HOST/excel/info" -F file=@$file -H  $token)
              echo $curl
              ;;
        "/image/convert")
              read -p "Enter a image (png or jpg) to convert [rocket.png]:" file
              file=${file:-rocket.png}
              curl=$(curl -s "$LOCAL_HOST/image/convert" -F file=@$file -H  $token)
              echo $curl

              read -p "Print to file inside this folder? [1]" yes
              yes=${yes:-y}

              if [ $yes = y ]
              then
                  curl=$(curl -s "$LOCAL_HOST/image/convert" -F file=@$file -H  $token >> output)
                  echo $curl
                  echo 'check for output file'
              fi

            ;;
        "/image/convert/fromdropbox")

              echo "Enter DROPBOX URL to image (png or jpg):"
              read url
              curl=$(curl -s "$LOCAL_HOST/image/convert/fromdropbox" -F url="$url" -H  $token)
              echo $curl

              read -p "Print to file inside this folder? [y]" yes
              yes=${yes:-y}

              if [ $yes = y ]
              then
                  curl=$(curl -s "$LOCAL_HOST/image/convert/fromdropbox" -F url="$url" -H  $token >> dropboxoutput)
                  echo $curl
                  echo 'check for dropboxoutput'
              fi
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
