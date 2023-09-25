# Consumer

Service instance responsible for consuming events, such as the creation of new orders for the authenticated users.

Several instances may be initialized at the same time.

## Installing

### Local

- Create a `.env` file based on the example available. Default values are used by the **compose.yaml** file.
- Create a virtual environment
- Install all the dependencies
- Run the script

```bash
python3.10 -m pipenv shell
pipenv sync
python main.py
```
