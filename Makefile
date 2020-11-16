default: data
	hugo

serve: data
	hugo -D server

clean:
	rm -rf public

data:
	python3 tools/generate_data.py
