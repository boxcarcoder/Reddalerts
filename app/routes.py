from app import app

@app.route('/')
@app.route('/index')

# Route handlers are written as Python functions, 
# called view functions.
def index():
    return ""