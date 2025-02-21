from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

def execute_code(language, code):
    if language == 'python':
        return execute_python(code)
    elif language == 'c':
        return execute_c(code)
    elif language == 'cpp':
        return execute_cpp(code)
    elif language == 'java':
        return execute_java(code)
    else:
        return "Unsupported language"

def execute_python(code):
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return "Code executed successfully"
    except Exception as e:
        return str(e)

def execute_c(code):
    with open('temp.c', 'w') as f:
        f.write(code)
    
    try:
        subprocess.run(['gcc', 'temp.c', '-o', 'temp'], check=True)
        result = subprocess.run(['./temp'], capture_output=True, text=True)
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        return str(e)

def execute_cpp(code):
    with open('temp.cpp', 'w') as f:
        f.write(code)
    
    try:
        subprocess.run(['g++', 'temp.cpp', '-o', 'temp'], check=True)
        result = subprocess.run(['./temp'], capture_output=True, text=True)
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        return str(e)

def execute_java(code):
    with open('Temp.java', 'w') as f:
        f.write(code)
    
    try:
        subprocess.run(['javac', 'Temp.java'], check=True)
        result = subprocess.run(['java', 'Temp'], capture_output=True, text=True)
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debug', methods=['POST'])
def debug():
    data = request.json
    language = data['language']
    code = data['code']
    output = execute_code(language, code)
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
