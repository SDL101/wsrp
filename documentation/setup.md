---
id: setup
---

# Setup Instructions

- [Setup Instructions](#setup-instructions)
  - [1. Virtual Environment](#1-virtual-environment)
    - [Install VirtualBox](#install-virtualbox)
    - [Install Ubuntu 22.04 LTS (Virtual Machine)](#install-ubuntu-2204-lts-virtual-machine)
    - [Install Required Packages](#install-required-packages)
    - [Clone This Repository](#clone-this-repository)
  - [2. Database](#2-database)
  - [3. Server](#3-server)
  - [4. Front End](#4-front-end)
  - [Wrapping up](#wrapping-up)

This document walks through step by step the process to run the application on your local machine. Everything needed to install and launch the application is included in this repository. 

The application itself is a lightweight banking application, in which a user can log in as a customer or an employee, access account details and view transactions. 

The database is a MySQL relational database. The server is a Python Flask application, and the front end uses the Vue.js framework. 

> [!WARNING]
> Beacuse of the security vulnerabilities intentionally included in this application, we advise anyone trying it out to do so inside of a virtual machine. We have chosen VirtualBox running an instance of Ubuntu 22.04 as our virtual environment, which is covered in [below](#virtual-environment).

There are four main steps to set up this project in order to interact with it:

1. Set up virtual environment
2. Create and run database instance
3. Set up Flask server
4. Set up Vue.js front end

These steps should be completed in order. 

## Logging in

Here are user login credentials to use to test different users, "rwilson" is an EMPLOYEE, and "jsmith" is a CUSTOMER.

```bash
user_name: rwilson
passowrd: password123

user_name: jsmith
password: easierpass
```


## 1. Virtual Environment

### Install VirtualBox

[Oracle VirtualBox](https://www.virtualbox.org/) is a free tool that lets you run **virtual machines (VMs)** on your computer. You’ll need it to create a separate, controlled environment for this project.

1. Download and install **VirtualBox** from:  
   🔗 [https://www.virtualbox.org/](https://www.virtualbox.org/)

---

### Install Ubuntu 22.04 LTS (Virtual Machine)

🖥 **What is Ubuntu & Why are We Using It?**  
Ubuntu is a popular, free **Linux-based operating system**. We use it because it provides a secure and consistent development environment that closely resembles real-world web servers.

To set up an **Ubuntu virtual machine (VM)**:

1. Download Ubuntu 22.04 LTS (or later) from:  
   🔗 [https://releases.ubuntu.com/jammy/](https://releases.ubuntu.com/jammy/)
2. Open **VirtualBox**, click **New**, and:
   - Name: `Ubuntu 22.04` or current
   - Type: `Linux`
   - Version: `Ubuntu (64-bit)` or appropriate option for your machine
   - Memory: At least **??GB RAM** (recommended)
   - Storage: At least **??GB+ dynamically allocated disk**
3. Attach the **Ubuntu ISO** and install it inside the VM.
4. Once installed, **log into Ubuntu** and open a **terminal** .

---

### Install Required Packages

Inside the **Ubuntu terminal**, run:

```bash
sudo apt update && sudo apt install git python3.10-venv curl -y
```

- `git` → Needed to clone the project repository.
- `python3.10-venv` → Creates an isolated Python environment.
- `curl` → Fetches files from the web.

---

### Clone This Repository

Once Ubuntu is set up, **clone the project** into your virtual environment:

```bash
git clone https://github.com/ted-miller92/wsrp.git
cd wsrp
```

## 2. Database

These are the steps to install and set up postgresql database in linux environment

Install postgresql

```bash
sudo apt install postgresql
```

Open postgresql as the "postgres" user: 

```bash
sudo -u postgres psql
```

You should now have a terminal with a prompt that looks like:

```bash
postgres=#
```

Create the database:

```bash
CREATE DATABASE banking_db_v0;
```

Now, create a user with a password. This username and password will be the one to include later in the .env file 

```bash
create user server_user with encrypted password 'server_pass';
```

Now grant privileges to that user: 

```bash
grant all privileges on database banking_db_v0 to server_user;
exit;
```

Now, navigate to the directory that has the file "database_setup_postgres.sql". Enter the following:

```bash
psql -h 127.0.0.1 -d banking_db_v0 -U postgres -p 5432 -f database_setup_postgres.sql
```

Restart the postgres service:

```bash
sudo systemctl restart postgresql
```

Then check the status:

```bash
sudo systemctl status postgresql
```

## 3. Server

Navigate to the server directory with `cd server`.

Create a python virtual environment, then activate it:

```bash
python3 -m venv server_env
source server_env/bin/activate
```
Install the required packagegs and then run the app:

```bash
pip install -r requirements.txt
flask --app server.py run
```

At this point you should be able to access the API endpoints in the browser. 

## 4. Front End

Navigate to the `wsrp_vue` directory.

Vue.js runs on Node. We will use Node Version Manager (`nvm`) to install Node. 

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
```

Verify version:

```bash
nvm --version
```

Should show the version specified in the `curl` command above. Now install Node:

```bash
nvm install node
```

The latest version will be installed. Double check that you are in the `wsrp_vue` directory then install dependencies:

```bash
npm install
```

Run the front end server:

```bash
npm run dev
```

You should now be able to access the application at the URL printed in the terminal. 

![vue serverv output](./images/vue_output.png)

## Wrapping up

Now you should be able to access the application at the URL printed in the terminal. 

**Continue to the [Exploration Guide](exploration_guide.md) to start hacking!**
