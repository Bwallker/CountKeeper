import pattern_parts.components as components


def optimize(component: components.Component) -> components.Component:
    new_component, changes_made = component.optimize(None)
    while changes_made:
        new_component, changes_made = new_component.optimize(None)
    return new_component
