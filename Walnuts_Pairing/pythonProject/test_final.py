import os
import shutil

# Clean up test folders
ROOT_FOLDER = 'data'

if os.path.exists(ROOT_FOLDER):
    for size_folder in os.listdir(ROOT_FOLDER):
        size_path = os.path.join(ROOT_FOLDER, size_folder)
        if os.path.isdir(size_path):
            print(f"Cleaning size folder: {size_folder}")
            # Remove all collection folders
            for collection_folder in os.listdir(size_path):
                collection_path = os.path.join(size_path, collection_folder)
                if os.path.isdir(collection_path):
                    shutil.rmtree(collection_path)
                    print(f"  Removed collection: {collection_folder}")
            # Remove empty size folder
            if not os.listdir(size_path):
                os.rmdir(size_path)
                print(f"  Removed empty size folder: {size_folder}")

print("All test folders cleaned up.")

# Final verification - check if any test folders remain
if os.path.exists(ROOT_FOLDER) and not os.listdir(ROOT_FOLDER):
    os.rmdir(ROOT_FOLDER)
    print("Removed empty root folder.")

print("Cleanup completed.")