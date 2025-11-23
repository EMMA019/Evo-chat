from app import create_app

# Create Flask application instance from application factory
app = create_app()

if __name__ == '__main__':
    # Start development server
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)