
# Microsoft Rewards Famer (MSRF)

This project is a automated farmer for Microsoft Rewards. It will log into given accounts and complete surveys, quizzes, and conduct bing searches. The farmer will automatically schedule runs to farm points for each account. More details on what exactly it is doing is outlined below.

**Usage of this application may get your Microsoft account permanently banned. I take no responsibility for any actions made on your account.**

This project is a rewrite of ["Microsoft-Rewards-Farmer"](https://github.com/charlesbel/Microsoft-Rewards-Farmer). The goal of this project is to move towards a documented and test driven code base. The entire code base has been restructured, and over 90% of it is re-written. Some components from the original project still exist within this one.

## Demo
[[demo/demo-add-account.png|Add Account Demo]]

## Installation

Download the zip file from the Github releases for this project. It will include everything needed to run this program, including: 
  - The main executable
  - Chrome
  - Chromedriver Binary

Run the executable to start the program.

*Note: The bundled Chrome and Chromedriver binaries will likely be outdated. This is to prevent breaking changes in Chrome and Chromedriver from affecting the program. For every major release, both bundled binaries will be updated. When using this program, you accept the risk of using unsecure software that may compromise the overall security of your system.

## Development

This project was developed in Python 3.10.8 and has **not** been tested with any other version of python. 

Install all python dependencies using the `requirements.txt` file found in the root of this project. 

```bash
python -m pip install -r requirements.txt
```

Selenium requires a Chromedriver binary and Chrome installation. This is automatically detected assuming you have correctly configured both on your machine.
This behavior can be changed temporarily for development. Browser initialization is done in the file `./util/browser/browser_setup.py`. Here you can configure custom chromedriver and chrome binary paths.

## Information
### Yields
I haven't recorded any numbers for how well this works. I do know that not all quizzes will be completed, sometimes the daily set won't fully complete, and you may not get the streak for that day. 
If the quiz types change, or new data is present that I have not designed this farmer around, they will not be completed. 

That being said, from my testing and observation, a level 2 microsoft rewards account seems to get 150-250 points per day. 
This number can be increased by manually ensuring that the daily set is completed, so that you gain streak bonuses, and that any additional quizzes or polls that the bot is unable to do are completed. 

### Bans
I've been developing this for about a month now. I haven't been banned on the 4 accounts that I have been testing on. After redeeming excess of $25 worth of rewards, and continuously running this daily, not one account has been banned. 

Microsoft may change their methods of banning at any time. Use accounts that you do not value, and redeem your reward as soon as you have enough points. 

I'm also not currently aware of any IP bans or rate limits for a single IP when it comes to point collection and reward redemption, as I haven't encountered this in my testing. If this concerns you, i advise you use a VPN. If this becomes a major problem I may incorporate proxy servers into this project.

### Breaking Changes
Microsoft can make changes at any time. They may break the farmer. I've designed this so that whichever component doesn't work, is simply skipped, outputting a critical error then continuing to the next task. 
When breaking changes are known, I will work towards fixing them. 


## Contributing

There are no contributing guidelines (for now). 


## 🚀 About Me
I'm a developer. Actively learning and looking for new and interesting opportunities. Send me a message: aryan@aryankothari.dev


## License

[MIT](https://choosealicense.com/licenses/mit/)

