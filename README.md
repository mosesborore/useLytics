# useLytics - Mixed Stuff Management System

## How to use it

1. Clone this repo
    - the project is in a folder called useLytics/useLytics
    - How to run the project
    ```bash
        # create virtual environment
        python3 -m venv .venv

        # activate the venv
        source .venv/bin/activate

        # install pip packages
        pip install -r ./useLytics/requirements.txt

        # cd into the project
        cd useLytics/

        # install tailwind
        npm i

        # run the server
        python3 manage.py runserver 0.0.0.0:8000

        # open another terminal tab, run
        cd useLytics/uselytics
        npm run watch:css
    ```
