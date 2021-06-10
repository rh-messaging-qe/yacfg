# Getting started

* Python 3.6+
* current requirements from setup.py (runtime requirements only)
* python virtualenv recommended (install via system package manager
or `pip install --user virtualenv`)

for contributors:
* requirements from requirements.txt (there are Dev and QA requirements as well)

## From git

```bash
git clone https://github.com/rh-messaging-qe/yacfg.git
python -m virtualenv -p python3 venv3
source venv3/bin/activate
./setup.py install
yacfg --help
```

## From PyPI

```bash
python -m virtualenv -p python3 venv3
source venv3/bin/activate
pip install yacfg
yacfg --help
```
