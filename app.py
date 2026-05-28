import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Base directory jahan saare custom project folders rahenge
PROJECTS_DIR = os.path.join('static', 'projects')

# Agar projects dir nahi bana hai, toh initialization ke waqt use bana dein
if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

# Utility function: Saare available folders ki list nikalne ke liye
def get_all_folders():
    if os.path.exists(PROJECTS_DIR):
        return [f for f in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, f))]
    return []

@app.route('/')
def home():
    # Saare manually ya github se banaye huye folders auto-detect honge
    folders = get_all_folders()
    
    # URL query parameter se select kiya hua folder get karein
    selected_folder = request.args.get('folder')
    
    # Default behavior: Agar koi folder selected nahi hai toh list ka pehla folder uthao
    if not selected_folder and folders:
        selected_folder = folders[0]
        
    code_content = ""
    image_path = None
    
    if selected_folder:
        current_folder_path = os.path.join(PROJECTS_DIR, selected_folder)
        
        # Selected folder ke andar se analysis.py ka code read karein
        code_file_path = os.path.join(current_folder_path, 'analysis.py')
        if os.path.exists(code_file_path):
            with open(code_file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
                
        # Us folder ke andar se image file check karein
        for ext in ['png', 'jpg', 'jpeg', 'webp', 'svg']:
            potential_img = f'output.{ext}'
            if os.path.exists(os.path.join(current_folder_path, potential_img)):
                image_path = f'static/projects/{selected_folder}/{potential_img}'
                break

    return render_template(
        'index.html', 
        folders_list=folders, 
        selected_folder=selected_folder, 
        code=code_content, 
        image=image_path
    )

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        folder_option = request.form.get('project_folder')
        code_data = request.form.get('code')
        uploaded_image = request.files.get('image')
        
        target_folder = folder_option
        
        if folder_option == '__NEW__':
            new_folder_name = request.form.get('new_folder_name')
            if new_folder_name:
                target_folder = new_folder_name.strip()
                
        target_path = os.path.join(PROJECTS_DIR, target_folder)
        
        if not os.path.exists(target_path):
            os.makedirs(target_path)
            
        # Python source code save karein
        if code_data:
            with open(os.path.join(target_path, 'analysis.py'), 'w', encoding='utf-8') as f:
                f.write(code_data)
                
        # Uploaded image save karein
        if uploaded_image and uploaded_image.filename != '':
            ext = uploaded_image.filename.split('.')[-1].lower()
            if ext in ['png', 'jpg', 'jpeg', 'webp', 'svg']:
                img_save_path = os.path.join(target_path, f'output.{ext}')
                uploaded_image.save(img_save_path)
                
        return redirect('/')
        
    return render_template('admin.html', existing_folders=get_all_folders())

if __name__ == '__main__':
    app.run(debug=True, port=8080)
