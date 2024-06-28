import h5py

def print_hdf5_structure(name, obj):
    if isinstance(obj, h5py.Group):
        print(f"Group: {name}")
    elif isinstance(obj, h5py.Dataset):
        print(f"  Dataset: {name}")
        print(f"    Shape: {obj.shape}")
        print(f"    Dtype: {obj.dtype}")
    else:
        print(f"Unknown item: {name}")

    # Print attributes if they exist
    if obj.attrs:
        print(f"    Attributes of {name}:")
        for key, val in obj.attrs.items():
            print(f"      {key}: {val}")

def traverse_hdf5_group(group, prefix=''):
    for key in group.keys():
        item = group[key]
        item_name = f"{prefix}/{key}"
        print_hdf5_structure(item_name, item)
        if isinstance(item, h5py.Group):
            traverse_hdf5_group(item, prefix=item_name)

# Replace 'PureFusionMaterials_libv1.hdf5' with the correct path to your HDF5 file
file_path = 'PureFusionMaterials_libv1.hdf5'

try:
    with h5py.File(file_path, 'r') as f:
        traverse_hdf5_group(f)
except OSError as e:
    print(f"Error opening file: {e}")
