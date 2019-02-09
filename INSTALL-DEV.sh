python -m venv env
. env/bin/activate
python -m pip install pip --upgrade pip
pip install --upgrade setuptools
pip install -e ".[test]"