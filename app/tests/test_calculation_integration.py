name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  test-and-build:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: fastapi_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U postgres"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        env:
          DATABASE_URL: postgresql+psycopg://postgres:postgres@localhost:5432/fastapi_db
        run: pytest

      - name: Log in to Docker Hub
        if: github.ref == 'refs/heads/main'
        run: echo "${{ secrets.DOCKERHUB_PASSWORD }}" | docker login -u "${{ secrets.DOCKERHUB_USERNAME }}" --password-stdin

      - name: Build Docker image
        if: github.ref == 'refs/heads/main'
        run: docker build -t ${{ secrets.DOCKERHUB_USERNAME }}/fastapi-calculator-stack:latest .

      - name: Push Docker image
        if: github.ref == 'refs/heads/main'
        run: docker push ${{ secrets.DOCKERHUB_USERNAME }}/fastapi-calculator-stack:latest