# Click-counter #

## Description ## 

The script allows you to shorten links using the API [bit.ly](https://app.bitly.com/) and find out the number of clicks on the abbreviated link.

## How to install ##

Python should be already installed. 
Use `pip`(or `pip3` for Python3) to install dependencies:

```commandline
pip install -r requirements.txt
```

## Launch ##
Add 'BITLY_TOKEN' to .env file.

Run `python main.py` with the arguments as links you want to shorten and get bit links.

```commandline
python main.py google.com
```

If you set Bitlinks as a parameters the program will count the number of clicks on it.

```commandline
python main.py bit.ly/3RIhPD9
```
