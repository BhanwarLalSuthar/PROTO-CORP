import open3d as o3d
import numpy as np

# Load a mesh file
mesh = o3d.io.read_triangle_mesh("model.stl")


# Ensure the mesh has triangles
mesh.compute_triangle_normals()

if not mesh.has_triangles():
    print("Mesh has no triangles! Trying to remesh...")
    mesh = mesh.subdivide_midpoint(number_of_iterations=1)  # Attempt to add faces

# Sample points
pcd = mesh.sample_points_uniformly(number_of_points=5000)

# Save point cloud
o3d.io.write_point_cloud("mesh_point_cloud1.ply", pcd)



# # Generate random points (for example, a cube-shaped cloud)
# num_points = 5000
# points = np.random.uniform(-1, 1, (num_points, 3))  # Random points in 3D space

# # Create Open3D PointCloud object
# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(points)

# # Save in different formats
# o3d.io.write_point_cloud("point_cloud.ply", pcd)  # Save as PLY
# o3d.io.write_point_cloud("point_cloud.pcd", pcd)  # Save as PCD
# np.savetxt("point_cloud.xyz", points, fmt="%.6f")  # Save as XYZ
