# Dear_Ocean_Digital_Coral_Ark_Bot

## Intro

This tool was made to support the Dear Ocean Digital Coral Ark project. The goals of the Dear Ocean Digital Coral Ark Project are outlined below 

```txt
Dear Ocean is currently compiling a longitudinal photo and video library of at-risk coral reefs by crowdsourcing historical, current, and future footage. The focus will be on smaller reef systems that may not be well-documented by the larger conservation organizations, but are nonetheless popular with snorkelers and divers.
```

This tool is used to automate the process of moving files from a user's local machine to the postgres database where we maintain our digital records. It also assists with the menial task of renaming files. 

## Instructions

```sh

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python app.py

```

## Correct format 

Example Correct Format: 

2016-01-31_HAN_BLUEBTR_0000000_TAGBG_0000001_Roberts_a.jpg




