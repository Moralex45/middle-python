from app_utils import create_raw_app


def main():
    app = create_raw_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
