# I want to share my data with others

we are going to need to host our data on a server. Lets make our data stack available 100% of the time with Mother Duck 🦆

MotherDuck is a cloud service that hosts your DuckDB tables. Rather than pointing DuckDB at a single database file on disk, you can point it at a cloud-hosted database that can be accessed anywhere with high performance, just like any other cloud data warehouse like Snowflake or BigQuery.


Head on over to [app.motherduck.com](https://app.motherduck.com/) to create an account and get an access token.

Then in your terminal export the token as an env variable like so:

```bash
export motherduck_token=<token>

# and change the environment to production with

export NSW_DOE_DATA_STACK_IN_A_BOX__ENV="prod" # you can also change it in the .env file but will require a reload of your env.

# then run your dagster pipeline in prodution
task dag
```

📒 Normally i would put this in the .env file. But as i want to commit my .env file to enable a one click deployment with the limitation vscode python extension only allows one env file. VScode Python team wont support multiple .env files [Source](https://github.com/microsoft/vscode-python/issues/10142)