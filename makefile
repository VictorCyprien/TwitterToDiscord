install:
	python3 -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

run:
	. venv/bin/activate; python main.py	

clean:
	rm -R venv

build_image:
	docker build -t twitter_to_discord  .

build_container:
	docker run -d -it --name TwitterToDiscord --env-file .env --cpus="1" --memory="2048m" twitter_to_discord

remove_container:
	docker stop TwitterToDiscord && docker remove TwitterToDiscord

run_on_docker:
	make remove_container
	make build_image
	make build_container

logs:
	docker logs TwitterToDiscord -f

