# Amazebot - Amazon price tracker

Amazebot is a simple Amazon price tracker that helps you monitor the prices of your favorite products on Amazon.

### Built With

- Python
- Selenium
- Flask
- Vite 
- React
- Shadcn

## Getting Started

- Follow these steps to setup the project locally.


### Prerequisites

List of prerequisites required to run the project:
- Python
- NodeJs
- Git

### Installation

Step-by-step instructions on how to install the project:

1. Clone the repository:

```sh
git clone https://github.com/MustangBro7/amazebot
```
2. Switch into directory:

```sh
cd amazebot
```
3. Install all packages:

```sh
npm install
pip install -r requirements.txt
```
4. To run the project:
Open 2 different terminals the following commands in the different terminals

```sh
npm run build
```
```sh
python app.py
```

<a name="daily-usage"></a>
## Setting Up for Daily Usage
If you wish to just use this app to track the prices, open the frontend by going to this link :
https://amazebot-tracker.netlify.app/

### Setting up the backend 
#### Note: If you want this to actually work to its fullest , you will want the python script to be running at all times you need to schedule this script, here is how you do it.

1. Open task scheeduler
2. Click on create task
3. Give the task a name
4. Click oon triggers and click in new
5. Choose At start up in the 'begin task' dropdown
6. open terminal and run this comman :
```
where python
```
7. Copy the .exe file location 
8. Go to actions in the task scheduler menu and click on new
9. Type app.py into the Add arguments section 
10. Type the path into the 'Start in' box and click ok.