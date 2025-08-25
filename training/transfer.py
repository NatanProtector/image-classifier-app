import os
import shutil
from pathlib import Path

def transfer_images():
    """
    Transfer all images from men and women folders to other folder
    with renamed files using pattern: {folder}_{original_name}
    """
    # Define source and destination paths
    data_dir = Path("data")
    men_dir = data_dir / "men"
    women_dir = data_dir / "women"
    other_dir = data_dir / "other"
    
    # Ensure other directory exists
    other_dir.mkdir(exist_ok=True)
    
    # Function to transfer images from a source folder
    def transfer_folder_images(source_folder, folder_name):
        if not source_folder.exists():
            print(f"Source folder {source_folder} does not exist")
            return
        
        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'}
        image_files = [f for f in source_folder.iterdir() 
                      if f.is_file() and f.suffix.lower() in image_extensions]
        
        print(f"Found {len(image_files)} images in {folder_name} folder")
        
        transferred_count = 0
        for image_file in image_files:
            # Create new filename: {folder}_{original_name}
            new_filename = f"{folder_name}_{image_file.name}"
            destination_path = other_dir / new_filename
            
            # Check if destination file already exists
            if destination_path.exists():
                print(f"Warning: {new_filename} already exists, skipping...")
                continue
            
            try:
                # Copy the file
                shutil.copy2(image_file, destination_path)
                transferred_count += 1
                print(f"Transferred: {image_file.name} -> {new_filename}")
            except Exception as e:
                print(f"Error transferring {image_file.name}: {e}")
        
        print(f"Successfully transferred {transferred_count} images from {folder_name} folder")
        return transferred_count
    
    # Transfer images from men folder
    print("=" * 50)
    print("TRANSFERRING IMAGES FROM MEN FOLDER")
    print("=" * 50)
    men_count = transfer_folder_images(men_dir, "men")
    
    # Transfer images from women folder
    print("\n" + "=" * 50)
    print("TRANSFERRING IMAGES FROM WOMEN FOLDER")
    print("=" * 50)
    women_count = transfer_folder_images(women_dir, "women")
    
    # Summary
    print("\n" + "=" * 50)
    print("TRANSFER SUMMARY")
    print("=" * 50)
    print(f"Total images transferred from men: {men_count}")
    print(f"Total images transferred from women: {women_count}")
    print(f"Total images transferred: {men_count + women_count}")
    print("=" * 50)

if __name__ == "__main__":
    # Change to the script's directory to ensure relative paths work
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("Starting image transfer process...")
    transfer_images()
    print("Image transfer process completed!")