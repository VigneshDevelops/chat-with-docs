# run.py
import uvicorn


def main():
    uvicorn.run("app.main:app", reload=True)


if __name__ == "__main__":
    main()
