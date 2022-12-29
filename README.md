
# Microsoft Rewards Famer (MSRF)

This project is a automated farmer for Microsoft Rewards. It will log into given accounts and complete surveys, quizzes, and conduct bing searches. This application is primarily designed to be run in a server environment, as it will automatically schedule executions of the farmer. This is done to carefully control the frequency of runs on a single account, to avoid bans. 

**Usage of this application may get your Microsoft account permanently banned. I take no responsibility for any actions made on your account.**

This project is a rewrite of ["Microsoft-Rewards-Farmer"](https://github.com/charlesbel/Microsoft-Rewards-Farmer). The goal of this project is to move towards a documented and test driven code base. 
## Features

- Hands free farming
- Web interface for tracking points and recent executions


## Installation

The project has a few components to deploying for development.
- Database: Pocketbase
- Flask Server / Farmer Scripts
- Chromedriver (for selenium)


### Database

Don't ask why I'm using PocketBase. In the near future, the application will auto configure PocketBase in this project.

**WIP**

### Chromedriver
Currently, no specific Chromedriver version is required. The Chromedriver must be in the PATH as Selenium auto detects this. In the near future, the application will auto configure Chromedriver within the project. 

**WIP**

### Flask Server / Farmer Scripts

Clone this repository and navigate to the root of the project. 

```bash
  python -m pip install -r requirements.txt
```

Database must be active for this to work. 

```bash
python main.py
```

This will schedule tasks to run the farmer when applicable. It will also start the web interface. 

## Documentation
TBD

The documentation for this project will be created late in the development cycle, as many things are currently changing. 


## Roadmap

- Add tests to identify breaking changes to Microsoft Rewards.

- Add CLI for generic use. 

## Contributing

There are no contributing guidelines (for now). 


## 🚀 About Me
I'm a developer. Actively learning and looking for new and interesting opportunities. Send me a message: aryan@aryankothari.dev


## License

[MIT](https://choosealicense.com/licenses/mit/)

