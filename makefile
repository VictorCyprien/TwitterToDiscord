install:
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

run:
	. venv/bin/activate; python main.py	

clean:
	rm -R venv

build_image:
	docker build -t twitter-to-discord:latest  .

build_container:
	docker run -d -it --name TwitterToDiscord --env-file .env --cpus="1" --memory="2048m" twitter-to-discord

remove_container:
	docker stop twitter-to-discord && docker remove twitter-to-discord

logs:
	docker logs twitter-to-discord -f

build_db:
	docker image pull mongo
	docker volume create TwitterToDiscordData
	docker run -it -d -v TwitterToDiscordData:/data/db -p 127.0.0.1:27017:27017 --name TwitterToDiscordMongoDB mongo

clean_db:
	docker stop TwitterToDiscordMongoDB
	docker remove TwitterToDiscordMongoDB
	docker volume rm TwitterToDiscordData
