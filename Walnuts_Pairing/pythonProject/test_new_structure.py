import requests
import base64
import os
import glob

# Test login
def test_login():
    login_url = 'http://localhost:5000/login'
    data = {'username': 'admin', 'password': '123456'}
    response = requests.post(login_url, json=data)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        print(f"Login failed: {response.text}")
        return None

# Test upload images
def test_upload(token):
    upload_url = 'http://localhost:5000/upload'
    headers = {'Authorization': f'Bearer {token}'}
    
    # Load test images
    test_images = []
    for filename in glob.glob('*.png')[:6]:
        with open(filename, 'rb') as f:
            img_data = f.read()
            base64_img = base64.b64encode(img_data).decode('utf-8')
            test_images.append(base64_img)
    
    if len(test_images) < 6:
        print("Need at least 6 PNG images for testing")
        return []
    
    # Upload images
    file_ids = []
    for i, img_data in enumerate(test_images):
        data = {
            'image': img_data,
            'purpose': 'collection',
            'angle': 'top'
        }
        response = requests.post(upload_url, json=data, headers=headers)
        if response.status_code == 200:
            file_ids.append(response.json().get('file_id'))
        else:
            print(f"Upload image {i+1} failed: {response.text}")
    
    return file_ids

# Test collection
def test_collection(token, file_ids, size=33):
    collection_url = 'http://localhost:5000/collection'
    headers = {'Authorization': f'Bearer {token}'}
    
    data = {
        'images': file_ids,
        'size': size,
        'angles': ['top', 'bottom', 'left', 'right', 'front', 'back']
    }
    
    response = requests.post(collection_url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Collection successful: {response.json()}")
        return response.json().get('collection_id')
    else:
        print(f"Collection failed: {response.text}")
        return None

# Check directory structure
def check_directory_structure(size, collection_id):
    root_folder = 'data'
    size_folder = os.path.join(root_folder, str(size))
    collection_folder = os.path.join(size_folder, collection_id)
    
    if os.path.exists(collection_folder):
        print(f"✓ Collection folder exists: {collection_folder}")
        
        # Check images
        images = glob.glob(os.path.join(collection_folder, '*.png'))
        if len(images) >= 6:
            print(f"✓ Found {len(images)} PNG images in the collection folder")
            
            # Check naming convention
            for img_path in images:
                filename = os.path.basename(img_path)
                if '_' in filename and filename.endswith('.png'):
                    print(f"  - Image name: {filename} (follows naming convention)")
        else:
            print(f"✗ Only found {len(images)} images (expected 6)")
    else:
        print(f"✗ Collection folder does not exist: {collection_folder}")

if __name__ == "__main__":
    # Login
    token = test_login()
    if not token:
        exit()
    
    # Upload images
    file_ids = test_upload(token)
    if len(file_ids) < 6:
        exit()
    
    # Create collection
    collection_id = test_collection(token, file_ids, size=33)
    if not collection_id:
        exit()
    
    # Check directory structure
    check_directory_structure(33, collection_id)