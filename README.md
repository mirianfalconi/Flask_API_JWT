# Flask API

A basic API with
- JWT authentication between servers;
- organize tabs from the excel file;
- convert images into PNG or JPG from dropbox or file.
- Unit tests




## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash

sudo apt install python3-venv
python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt

export FLASK_APP=index.py
export SECRET_KEY='SECRET'

# Into tests/generate_jwt.py and __init__.py
DROPBOX_TOKEN = "NEEDS A GENERATED TOKEN"
SECRET_KEY = "SECRET"

flask run

#SECRET_KEY needs to be exported in ctx
#.env activated
py.test ##To run units tests


```

## Interative Bash

```bash

cd test
chmod +x testing.sh
./testing.sh


```

## License
[MIT](https://choosealicense.com/licenses/mit/)
