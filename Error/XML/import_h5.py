import h5py

def print_hdf5_structure(name, obj):
    if isinstance(obj, h5py.Group):
        print(f"Group: {name}")
    elif isinstance(obj, h5py.Dataset):
        print(f"Dataset: {name}, shape: {obj.shape}, dtype: {obj.dtype}")
    else:
        print(f"Unknown item: {name}")

    # Print attributes if they exist
    for key, val in obj.attrs.items():
        print(f"    Attribute: {key} = {val}")

# Replace 'PureFusionMaterials_libv1.hdf5' with the correct path to your HDF5 file
file_path = 'PureFusionMaterials_libv1.h5'

try:
    with h5py.File(file_path, 'r') as f:
        # Traverse the entire file structure
        f.visititems(print_hdf5_structure)
except OSError as e:
    print(f"Error opening file: {e}")
