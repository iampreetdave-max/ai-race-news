.PHONY: install scrape schedule api stats clean test

install:
	pip install -r requirements.txt

scrape:
	python run.py

schedule:
	python run.py --schedule

api:
	python run.py --api

stats:
	python run.py --stats

clean:
	python run.py --cleanup 30

test:
	pytest tests/ -v

docker-up:
	docker-compose up -d --build

docker-down:
	docker-compose down
