from rest_framework.routers import DefaultRouter, DynamicRoute, Route


def extend_detail_route(routes: list[Route | DynamicRoute]) -> Route:
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
    routes = [
        extend_detail_route(DefaultRouter.routes),
    ]
    include_root_view = False
