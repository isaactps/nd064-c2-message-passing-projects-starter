def register_routes(api, app, root="api"):
    from app.udaconnect.controllers import api as udaconnect_personService

    api.add_namespace(udaconnect_personService, path=f"/{root}")
