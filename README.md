
# Microsoft Rewards Famer (MSRF)

This project is a automated farmer for Microsoft Rewards. It will log into given accounts and complete surveys, quizzes, and conduct bing searches. The farmer will automatically schedule runs to farm points for each account. More details on what exactly it is doing is outlined below.

**Usage of this application may get your Microsoft account permanently banned. I take no responsibility for any actions made on your account.**

This project is a rewrite of ["Microsoft-Rewards-Farmer"](https://github.com/charlesbel/Microsoft-Rewards-Farmer). The goal of this project is to move towards a documented and test driven code base. The entire code base has been restructured, and over 90% of it is re-written. Some components from the original project still exist within this one.


## Installation

Download the zip file from the Github releases for this project. It will include everything needed to run this program, including: 
  - The main executable
  - Chrome
  - Chromedriver Binary

Run the executable to start the program.


## Development

This project was developed in Python 3.10.8 and has **not** been tested with any other version of python. 

Install all python dependencies using the `requirements.txt` file found in the root of this project. 

```bash
python -m pip install -r requirements.txt
```

Selenium requires a Chromedriver binary and Chrome installation. This is automatically detected assuming you have correctly configured both on your machine.
This behavior can be changed temporarily for development. Browser initialization is done in the file `./util/browser/browser_setup.py`. Here you can configure custom chromedriver and chrome binary paths.


## Contributing

There are no contributing guidelines (for now). 


## 🚀 About Me
I'm a developer. Actively learning and looking for new and interesting opportunities. Send me a message: aryan@aryankothari.dev


## License

[MIT](https://choosealicense.com/licenses/mit/)

