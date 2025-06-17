from flask import Flask, request, jsonify, render_template, send_file
import os
from werkzeug.utils import secure_filename
from legal_analyzer import analyze_legal_document
from pdf_generator import generate_pdf_summary
import json
from datetime import datetime

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        # Secure the filename and add timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(file.filename)
        filename = f"{timestamp}_{filename}"
        
        # Save the file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Analyze the document
            analysis_results = analyze_legal_document(file_path)
            
            # Save analysis results to a JSON file
            summary_filename = f"summary_{filename.rsplit('.', 1)[0]}.json"
            summary_path = os.path.join(app.config['UPLOAD_FOLDER'], summary_filename)
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_results, f, indent=2)
            
            # Generate PDF summary
            pdf_filename = f"summary_{filename.rsplit('.', 1)[0]}.pdf"
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
            generate_pdf_summary(analysis_results, pdf_path)
            
            # Add file paths to the response
            analysis_results['file_path'] = file_path
            analysis_results['summary_path'] = summary_path
            analysis_results['pdf_path'] = pdf_path
            
            return jsonify(analysis_results)
            
        except Exception as e:
            return jsonify({'error': str(e)})
    
    return jsonify({'error': 'Invalid file type'})

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True) 