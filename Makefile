.PHONY: serve build clean firmware

serve:
	zola serve --drafts

serve-prod:
	zola serve

build:
	zola build

clean:
	rm -rf public/

# Regenerate firmware index from static/firmware/ contents.
# Re-runs automatically when any file in static/firmware/ changes.
firmware: $(wildcard static/firmware/*)
	python3 scripts/gen-firmware.py
