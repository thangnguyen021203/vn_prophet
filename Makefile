up:
	docker-compose up -d

down:
	docker-compose down --volumes-orphans


clean:
	rm -rf data
	
logs:
	docker-compose logs -f