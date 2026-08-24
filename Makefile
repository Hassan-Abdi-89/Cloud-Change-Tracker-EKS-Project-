test:
	pytest -q

run:
	uvicorn app.main:app --reload

build:
	docker build -t cloud-change-tracker:local .

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f
