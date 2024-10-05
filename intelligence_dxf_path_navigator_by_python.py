import ezdxf
import matplotlib.pyplot as plt
import numpy as np

# Load the DXF file
file_path = 'D:\OneDrive Personal (CN)\OneDrive\Coding LAB\Google CoLab\Amir\Path_Planning.dxf'  # Replace this with the path to your DXF file
doc = ezdxf.readfile(file_path)
msp = doc.modelspace()

# List all entities in the DXF file
for entity in msp:
    print(f"Entity type: {entity.dxftype()}, Entity details: {entity}")

# List specific details of certain entities
for entity in msp:
    if entity.dxftype() == 'LINE':
        start = entity.dxf.start
        end = entity.dxf.end
        print(f"LINE: Start: {start}, End: {end}")
    elif entity.dxftype() == 'CIRCLE':
        center = entity.dxf.center
        radius = entity.dxf.radius
        print(f"CIRCLE: Center: {center}, Radius: {radius}")
    elif entity.dxftype() == 'ARC':
        center = entity.dxf.center
        radius = entity.dxf.radius
        start_angle = entity.dxf.start_angle
        end_angle = entity.dxf.end_angle
        print(f"ARC: Center: {center}, Radius: {radius}, Start Angle: {start_angle}, End Angle: {end_angle}")
    elif entity.dxftype() == 'LWPOLYLINE':
        points = entity.get_points('xy')
        print(f"LWPOLYLINE: Points: {points}")

# Function to visualize DXF entities with a black background and white lines
def plot_dxf_entities_black_bg():
    fig, ax = plt.subplots()

    # Set black background
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Iterate over the entities and plot them
    for entity in msp:
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            ax.plot([start[0], end[0]], [start[1], end[1]], color='white', linewidth=2)

        elif entity.dxftype() == 'CIRCLE':
            center = entity.dxf.center
            radius = entity.dxf.radius
            circle = plt.Circle((center[0], center[1]), radius, fill=False, edgecolor='white', linewidth=2)
            ax.add_artist(circle)

        elif entity.dxftype() == 'ARC':
            center = entity.dxf.center
            radius = entity.dxf.radius
            start_angle = np.radians(entity.dxf.start_angle)
            end_angle = np.radians(entity.dxf.end_angle)
            arc_theta = np.linspace(start_angle, end_angle, 100)
            x_arc = center[0] + radius * np.cos(arc_theta)
            y_arc = center[1] + radius * np.sin(arc_theta)
            ax.plot(x_arc, y_arc, color='white', linewidth=2)

        elif entity.dxftype() == 'LWPOLYLINE' or entity.dxftype() == 'POLYLINE':
            points = entity.get_points('xy')
            x, y = zip(*points)
            ax.plot(x, y, color='white', linewidth=2)

        elif entity.dxftype() == 'ELLIPSE':
            center = entity.dxf.center
            major_axis = entity.dxf.major_axis
            ratio = entity.dxf.ratio

            # Handle rotation attribute (some ellipses may not have it)
            angle = entity.dxf.rotation if 'rotation' in dir(entity.dxf) else 0

            t = np.linspace(0, 2 * np.pi, 100)
            x_ellipse = center[0] + major_axis[0] * np.cos(t)
            y_ellipse = center[1] + major_axis[1] * np.sin(t) * ratio
            rotation_matrix = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                                        [np.sin(np.radians(angle)),  np.cos(np.radians(angle))]])
            xy_ellipse = np.dot(rotation_matrix, np.vstack([x_ellipse - center[0], y_ellipse - center[1]]))
            ax.plot(xy_ellipse[0] + center[0], xy_ellipse[1] + center[1], color='white', linewidth=2)

        elif entity.dxftype() == 'SPLINE':
            fit_points = entity.fit_points
            if len(fit_points) > 1:
                # Unpack only the x and y coordinates, ignore z
                x, y = zip(*[(p[0], p[1]) for p in fit_points])  # Ignore z-coordinate
                ax.plot(x, y, color='white', linewidth=2)

    # Remove grid and ticks
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # Set equal scaling and show the plot
    ax.set_aspect('equal')
    plt.show()

# Call the function to visualize the DXF entities
plot_dxf_entities_black_bg()

