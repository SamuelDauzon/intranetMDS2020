# Projet My Digital School

## Installation

```
git clone https://github.com/SamuelDauzon/intranetMDS2020
cd intranetMDS2020
python3 -m venv ../venv_intranet
source ../venv_intranet/bin/activate
pip install -r requirements.txt
cp intranet_phonecenter/example_dev_settings.py intranet_phonecenter/local_settings.py
python manage.py migrate

```