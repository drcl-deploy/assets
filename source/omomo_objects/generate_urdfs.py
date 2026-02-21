import trimesh
from pathlib import Path

dir_path = Path(__file__).parent

URDF_TEMPLATE = """<?xml version="1.0"?>
<robot name="{name}">

  <link name="base_link">
    
    <inertial>
      <mass value="{mass:.5f}"/>
      <inertia ixx="{ixx:.6f}" ixy="0.0" ixz="0.0" iyy="{iyy:.6f}" iyz="0.0" izz="{izz:.6f}"/>
    </inertial>

    <visual>
      <geometry>
        <mesh filename="{name}.obj"/>
      </geometry>
    </visual>

    <collision>
      <geometry>
        <mesh filename="{name}.obj"/>
      </geometry>
      <surface>
        <friction>
          <ode>
            <mu>0.6</mu>
            <mu2>0.6</mu2>
          </ode>
        </friction>
        <contact>
          <ode>
            <kp>1000000.0</kp>
            <kd>1.0</kd>
            <max_vel>100.0</max_vel>
            <min_depth>0.001</min_depth>
          </ode>
        </contact>
      </surface>
    </collision>
    
  </link>
</robot>
"""


def compute_inertia(mesh, mass: float = 1.0):
    """Compute inertia tensor from mesh assuming uniform density."""
    # Use trimesh to compute inertia (assumes density=1, then scale by mass)
    mesh.density = mass / mesh.volume if mesh.volume > 0 else 1.0
    inertia = mesh.moment_inertia
    return inertia[0, 0], inertia[1, 1], inertia[2, 2]


def generate_urdf(folder_path: Path):
    """Generate URDF file for a given folder containing an OBJ file."""
    folder_name = folder_path.name
    obj_file = folder_path / f"{folder_name}.obj"
    urdf_file = folder_path / f"{folder_name}.urdf"
    
    if not obj_file.exists():
        print(f"Skipping {folder_name}: No OBJ file found")
        return
    
    if urdf_file.exists():
        print(f"Skipping {folder_name}: URDF already exists")
        return
    
    # Load mesh
    mesh = trimesh.load(str(obj_file), force='mesh')
    
    # Estimate mass (default 1.0 kg, adjust as needed)
    mass = 1.0
    
    # Compute inertia
    try:
        ixx, iyy, izz = compute_inertia(mesh, mass)
    except Exception as e:
        print(f"Warning: Could not compute inertia for {folder_name}: {e}")
        # Use default small inertia values
        ixx = iyy = izz = 0.01
    
    # Generate URDF content
    urdf_content = URDF_TEMPLATE.format(
        name=folder_name,
        mass=mass,
        ixx=ixx,
        iyy=iyy,
        izz=izz,
    )
    
    # Write URDF file
    urdf_file.write_text(urdf_content)
    print(f"Created: {urdf_file}")


def main():
    """Generate URDFs for all object folders."""
    count = 0
    for folder in dir_path.iterdir():
        if folder.is_dir() and not folder.name.startswith('__'):
            generate_urdf(folder)
            count += 1
    
    print(f"\nProcessed {count} folders")


if __name__ == "__main__":
    main()