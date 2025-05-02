# To build the Docker image (from the same directory as the Dockerfile):
docker build -t md2htmlify-run .

# To run the container with the test_data directory mounted:
docker run -it --rm -v $(pwd)/test_data:/app/test_data md2htmlify-run