def register_routes(api, app, root="api"):
    from app.udaconnect.controllers import api as udaconnect_locationservice

    api.add_namespace(udaconnect_locationservice, path=f"/{root}")
