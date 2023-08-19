ALL :=                              \
    aiorise/events/event_types.py   \
    aiorise/api/response_types.py   \
    aiorise/api/request_types.py    \
    aiorise/objects/object_types.py \
    aiorise/api/client_methods.py   \


all: $(ALL)

aiorise/events/event_types.py: aiorise/codegen/generate_event_types.py api.json
	python -m aiorise.codegen.generate_event_types | python -m black - > $@

aiorise/api/response_types.py: aiorise/codegen/generate_response_types.py api.json
	python -m aiorise.codegen.generate_response_types | python -m black - > $@

aiorise/api/request_types.py: aiorise/codegen/generate_request_types.py api.json
	python -m aiorise.codegen.generate_request_types | python -m black - > $@

aiorise/objects/object_types.py: aiorise/codegen/generate_object_types.py api.json
	python -m aiorise.codegen.generate_object_types | python -m black - > $@

aiorise/api/client_methods.py: aiorise/codegen/generate_api_requests.py api.json
	python -m aiorise.codegen.generate_api_requests | python -m black - > $@

clean:
	rm -f $(ALL)

.PHONY: all clean
