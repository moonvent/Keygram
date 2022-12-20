# Keygram
<hr>

## Table of contents

1. [About](#about)
2. [Instruction](#instruction)
- [Setup dev environment](#setup_dev_environment)
- [Setup new language](#setup_new_language)

<a name='about'/>

## About
<hr>

<a name='instruction'/>

## Instruction
<hr>

<a name='setup_dev_environment'/>

### Setup dev environment

Project was write in [poetry](https://python-poetry.org/), but also have a standart reqs file (requirements.txt).
<br>
Better use the poetry, cause poetry more complex and functional then pip or pipenv, and poetry has a written scripts which make ease develop process.

<a name='setup_new_language'/>

### Setup new language

1. Copy language from directory locale (example en);
2. Change name on you need (example **<u>fr</u>**);
3. Entry in `src/locale/fr/LC_MESSAGE/Keygram.po`; 
4. Change all words on what you need (in section msgstr);

After that write this commands in terminal:

```
  msgfmt src/locale/fr/LC_MESSAGES/Keygram.po -o src/locale/en/LC_MESSAGES/Keygram.mo
```

Or you can run this command, if you install poetry

```
  poetry run update_langs
```

