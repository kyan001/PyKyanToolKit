py setup.py sdist
py setup.py bdist_wheel
py setup.py egg_info
twine upload dist/*
pip3 install --upgrade KyanToolKit