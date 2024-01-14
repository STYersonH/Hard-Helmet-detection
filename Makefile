build-docker:
	docker build -t hard-helmet-detection-python .

run-docker:
	docker run -p 5000:5000 hard-helmet-detection-python