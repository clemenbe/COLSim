def generate_grid(width, height):
    """Generates a grid of specified width and height and returns a list of all possible coordinates"""
    grid = []
    for x in range(width):
        for y in range(height):
            grid.append((x,y))
    return grid