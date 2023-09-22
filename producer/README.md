# Producer

The API responsible for producing events requisitions, such as the creation of new orders for the authenticated users.

## Installing

### Local

- Create a `.env` file based on the example available. Default values are used by the **compose.yaml** file.
- Create a virtual environment
- Install all the dependencies
- Run a local development server

```bash
python3.10 -m pipenv shell
pipenv sync
uvicorn app.main:app --reload
```
