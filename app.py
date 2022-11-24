from flask import Flask, render_template
import socket
app=Flask(__name__,  static_folder='')

def get_host_and_ip():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return str(host),str(ip)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    host,ip=get_host_and_ip()
    return render_template('health.html',HOST=host, IP = ip)

@app.route('/feature.html')
def feature():
    return render_template('feature.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'),500



if __name__ == '__main__':
    app.run(debug=True)