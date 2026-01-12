# Project structure rules

Please use this skill when you want to create/update new REST API resource.

The project structure is as follows:

```
./books-api/src/books_api
    ./http/MODEL/routes      # where we define the REST API.
    ./http/MODEL/schemas     # where we define the Response/Request schema for REST API resource.
    ./http/models/MODEL      # where we define the model in pydantic for the API resource.
    ./db/MODEL.py            # where we define the interaction with db for the API resource.
```

where MODEL is the REST resource.

Whenever adding a new resource, please ensure we have the same structure as above both for the src and tests
