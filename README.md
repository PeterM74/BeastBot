# BeastBot
<img src="https://img.shields.io/badge/build-development-yellow" />
BeastBot is a [Discord](https://discord.com/) bot for our gym group. It is currently a work in progress.

# Getting started
This will be complete for version 1.0. At the very least, you will need [Discord.py](https://discordpy.readthedocs.io/en/stable/) and other libraries specified in `requirements.txt`. Run the `requirements.txt` file in the console:

```commandline
pip install -r requirements.txt
```

You will also need to download some data:

```python
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
```

<!--- Update `requirements.txt` if doing development work
pipreqs --encoding=utf8 . --force --->