# Set up

1.  Clone locally

        git clone --recurse-submodules -j8  https://github.com/Impact-Africa-Network/expensly.git

2.  Create and activate virtual environment (Use `pipenv`)

        pipenv --python 3.10

        pipenv shell

        pipenv install

3.  Setup Database and Database User

        psql

        > create database expensly;

        > create role expensly with password 'expensly';

        > alter role expensly with login;

        > grant all on database expensly to expensly;

4.  Copy the contents of `example.env` to `.env` and populate the values appropriately.

        cp example.env .env

5.  Setup submodules

This Project relies on the following submodules:

`ian_account` - https://github.com/Impact-Africa-Network/ian-account (branch: `feat/expensly`)

`ian_auth` - https://github.com/Impact-Africa-Network/ian_auth. (branch: `feat/expensly`)

i. Initialize submodules

        git submodule init

ii. Fetch and update submodules

        git submodule update --remote --recursive

iii. Check out to the respective branches

        cd src/ian_auth

        git checkout feat/expensly


        cd src/ian_account

        git checkout feat/expensly

6.  Run migrations

        ./manage.py makemigrations

        ./manage.py migrate

### Authors

1. Kefa
2. Kabochi
3. Innocent

## Hat tip to everyone involved.
