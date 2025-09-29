# TF2Log

Yet another server browser for TF2. Inspired by [Battlelog](https://battlelog.battlefield.com/). Currently a work in progress.

## Setup

1. Create a virtual environment and install all the dependencies from requirements.txt

```bash
python -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
```

2. Create an `instance` directory and copy `config.json.example` as `config.json` in the the newly created `instance` directory

    - Set `ENV` to either `dev` or `prod` based on the environment
    - Set `TEAMWORK_TF_SECRET_KEY` to your [Teamwork.tf API key](https://teamwork.tf/settings)
    - Set `STEAMWORKS_SECRET_KEY` to your [Steam Web API key](https://steamcommunity.com/dev/apikey)
    - Set `CACHE_TYPE` to a [`flask-caching` backend](https://flask-caching.readthedocs.io/en/latest/#built-in-cache-backends), you probably want to use something like a Redis database in production
    - You also want to download the GeoLite2 City database in `.mmdb` format from [MaxMind](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data/) and place it in the instance directory

3. Run the application

    ```sh
    hypercorn "tf2log:create_app()"
    ```

## Licensing

TF2Log is licesed under [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.en.html).

SVG files are from [Bootstrap Icons](https://icons.getbootstrap.com/). Fonts are licensed under [SIL Open Font License 1.1](https://openfontlicense.org/) from their respective owners.
