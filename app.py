import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

PROJECTS_DIR = os.path.join('static', 'projects')

if not os.path.exists(PROJECTS_DIR):
    os.makedirs(PROJECTS_DIR)

def get_all_folders():
    if os.path.exists(PROJECTS_DIR):
        return [f for f in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, f))]
    return []

@app.route('/')
def home():
    folders = get_all_folders()
    selected_folder = request.args.get('folder')
    
    if not selected_folder and folders:
        selected_folder = folders[0]
        
    posts = [] # Saare serial wise posts isme aayenge
    
    if selected_folder:
        current_folder_path = os.path.join(PROJECTS_DIR, selected_folder)
        
        # Folder ke andar files scan karke serial numbers dhoondhein
        if os.path.exists(current_folder_path):
            files = os.listdir(current_folder_path)
            # Jetne bhi 'analysis_X.py' hain unke numbers nikalen
            serial_numbers = []
            for f in files:
                if f.startswith('analysis_') and f.endswith('.py'):
                    try:
                        num = int(f.split('_')[1].split('.')[0])
                        serial_numbers.append(num)
                    except:
                        pass
            
            # Serial wise sorting (1, 2, 3...)
            serial_numbers.sort()
            
            for num in serial_numbers:
                code_content = ""
                image_path = None
                
                # Code read karein
                code_file = os.path.join(current_folder_path, f'analysis_{num}.py')
                if os.path.exists(code_file):
                    with open(code_file, 'r', encoding='utf-8') as file_data:
                        code_content = file_data.read()
                
                # Image check karein
                for ext in ['png', 'jpg', 'jpeg', 'webp', 'svg']:
                    potential_img = f'output_{num}.{ext}'
                    if os.path.exists(os.path.join(current_folder_path, potential_img)):
                        image_path = f'static/projects/{selected_folder}/{potential_img}'
                        break
                
                posts.append({
                    'serial': num,
                    'code': code_content,
                    'image': image_path
                })

    return render_template(
        'index.html', 
        folders_list=folders, 
        selected_folder=selected_folder, 
        posts=posts # Ab single code ki jagah poori posts ki list ja rhi hai
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
            
        # 🔴 AUTOMATIC SERIAL NUMBER LOGIC
        files = os.listdir(target_path) if os.path.exists(target_path) else []
        existing_nums = [0]
        for f in files:
            if f.startswith('analysis_') and f.endswith('.py'):
                try:
                    existing_nums.append(int(f.split('_')[1].split('.')[0]))
                except:
                    pass
        next_serial = max(existing_nums) + 1 # Agla number (jaise 1, phir 2...)

        # Serial wise code file write karein
        if code_data:
            with open(os.path.join(target_path, f'analysis_{next_serial}.py'), 'w', encoding='utf-8') as f:
                f.write(code_data)
                
        # Serial wise image file save karein
        if uploaded_image and uploaded_image.filename != '':
            ext = uploaded_image.filename.split('.')[-1].lower()
            if ext in ['png', 'jpg', 'jpeg', 'webp', 'svg']:
                img_save_path = os.path.join(target_path, f'output_{next_serial}.{ext}')
                uploaded_image.save(img_save_path)
                
        return redirect('/')
        
    return render_template('admin.html', existing_folders=get_all_folders())

if __name__ == '__main__':
    app.run(debug=True, port=8080)
