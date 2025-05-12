
## Dream Team ✨
* [@aberguecio](https://github.com/aberguecio)
* [@mcox5](https://github.com/mcox5)
* [@hjmacaya](https://github.com/hjmacaya)
* [@lucasvsj](https://github.com/lucasvsj)

## Setup

### Backend (FastAPI)

   ```
   docker-compose -f docker-compose.dev.yml up --build
   ```

#### Local

1. Install Poetry:
   ```
   pip3 install poetry
   ```

2. Navigate to the backend directory:
   ```
   cd backend
   ```

3. Install dependencies:
   ```
   poetry install
   ```

4. Run the FastAPI server:
   ```
   poetry run uvicorn main:app --reload
   ```

#### Dockerisado

1. Crear Imagen

   ```
   docker build -t fastapi-app:python3.13 .
   ```

2. Correr Imagen
   ```
   docker run -p 8000:8000 fastapi-app:python3.13
   ```