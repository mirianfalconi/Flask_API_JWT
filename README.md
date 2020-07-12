# Flask API

A basic API with
- JWT authentication between servers;
- organize tabs from the excel file;
- convert images into PNG or JPG from dropbox or file.





## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash

sudo apt install python3-venv
python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt

export FLASK_APP=index.py
export SECRET_KEY='SECRET'

tests/generate_jwt.py
DROPBOX_TOKEN = "NEEDS A GENERATED TOKEN"
SECRET_KEY = "SECRET"

flask run

```

## To test

```bash

cd test
chmod +x excelInfo.sh
chmod +x convertImage.sh
chmod +x imageConvertFromdropbox.sh

./excelInfo.sh
./convertImage.sh
./imageConvertFromdropbox.sh

```

## License
[MIT](https://choosealicense.com/licenses/mit/)
