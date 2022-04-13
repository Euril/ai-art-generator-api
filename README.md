## Backend API Python Flask
Works alongside
[https://github.com/Euril/ai-art-generator-front-end]


<!-- # flask-api-auth-template

**Warning. This template should only be used if you are building out a Flask API.**

If you are building a Flask API back end, use the [Decoupled Mern JWT Auth Front End ](https://github.com/SEI-Remote/decoupled-mern-jwt-auth-template-front-end-photos) to create the corresponding React App. 

# Setup

Clone the template with the command below. Be sure to replace `<name-of-your-app-here>` in the commands below with the name of your app!

```bash
git clone https://github.com/SEI-Remote/flask-react-auth-template <name-of-your-app-here>
cd <name-of-your-app-here>
```

Once you are in the project directory:

```bash
rm -rf .git
```

Re-initialize a git repository:

```bash
git init
```

Use the GitHub CLI to create a new project repository on GitHub:

```bash
gh repo create <name-of-your-app-here>
```

# Getting Started

Create a new virtual environment for your project. The dependencies involved in this configuration of Flask (Flask API) are a bit different, so you’ll want a fresh start with this environment. 

```bash
conda create -n your_app python=3.9
```

Next, activate your virtual environment with the command below. 

```bash
conda activate your_app
```

Once the environment is active, run the following command in your terminal.

```bash
pip3 install -r requirements.txt 
```

In your terminal, run the following command to create a **`.env`** in the base directory of your project.

```bash
touch .env
```

Add an **`APP_SECRET`** variable to your **`.env`** file.

```
APP_SECRET=supersecretkey
```

Next up in the **`.env`**, add a `DATABASE_URL` with the name of our project’s database.

```
DATABASE_URL='postgresql://localhost:5432/your_database'
```

Make sure your conda environment is active and hop into the `psql` shell. Please run the following commands one at a time.

```
psql
```

```
create database your_database;
```

```
\q
```

```bash
python3 -m flask db init
python3 -m flask db migrate
python3 -m flask db upgrade
```

Run the following command to start your application.  start

```bash
python3 app.py
``` -->