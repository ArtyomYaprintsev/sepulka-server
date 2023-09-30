from rest_framework.routers import DefaultRouter, DynamicRoute, Route


def override_detail_route(routes: list[Route | DynamicRoute]) -> Route | None:
    """Find and override default detail route from the given routes.
    
    Replaces `lookup_kwarg` param in the found detail route with the static
    'me' string.

    Returns:
        Overridden the detail route if it exists in the given routes,
        `None` otherwise.
    """
    detail_route_index = None

    for index, route in enumerate(routes):
        if isinstance(route, Route) and route.detail:
            detail_route_index = index
            break

    if not detail_route_index:
        return

    return routes[detail_route_index]._replace(
        url=r'^{prefix}/me{trailing_slash}$',
    )


class PersonalOnlyRouter(DefaultRouter):
    """Provide detail route only with specified url.
    
    Uses `override_detail_route` to override default detail route.
    """

    routes = [
        override_detail_route(DefaultRouter.routes),
    ]
    include_root_view = False
