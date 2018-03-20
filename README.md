# Guide
---
## Installation
* Clone this repository then get into its directory
>```cd ./GLM-web-interface```
* edit .git/config if don't have the repository rights. Change this line:
> ```url = git@github.com:tomsimonart/GLM.git```

with
> ```url = https://github.com/tomsimonart/GLM.git```
* Install submodules
>```git submodule update --recursive```

## Starting
* Install python packages (**Using "**virtualenv**" is recommended**)
>```pip install -r requirements.txt```
* Start the server
>```python3 ./server.py 9999```
* Start flask
>```source launch.sh```

>```flask run```

## Web
* Url should be **[http://localhost:5000](http://localhost:5000)**
