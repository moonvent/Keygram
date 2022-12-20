# Keygram
<hr>

## Table of contents

1. [About](#about)
2. [Instruction](#instruction)
- [Setup dev environment](#setup_dev_environment)
- [Setup new language](#setup_new_language)
- [Add new db migration](#add_new_migration)

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

<a name='add_new_migration'/>

### Add new db migration

1. Project use ```sqlalchemy```, and ```alembic``` for work with migrations;
2. For create a new migratione entry in terminal and change directory to ```src/```;
3. Write command ```alembic revision -m "What you do in this revision message"``` and execute it;
4. After that, alembic create a file in ```src/alembic/versions/``` with end of your revision message, enter it;
5. In this file you have a two method, upgrade and downgrade, add in upgrade what you need, and in downgrade what you need if you want downgrade in future;
6. Leave from file and write a command ```alembic upgrade head```.
7. Excelent!

More detail you found in [docs](https://alembic.sqlalchemy.org/en/latest/tutorial.html) to alembic
