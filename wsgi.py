from app import create_app

app = create_app()

if __name__ == "__main__":
    # Keep debug=True to match your original; flip to False for production
    app.run(debug=True)
