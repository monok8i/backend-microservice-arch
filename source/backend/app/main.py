import uvicorn

from app.core import get_apiv1_app, get_apiv2_app

apiv1 = get_apiv1_app()
apiv2 = get_apiv2_app()

apiv1.mount("/v2", app=apiv2)


def main() -> None:
    uvicorn.run(
        app=apiv1,
        host="0.0.0.0",
        port=50,
    )


if __name__ == "__main__":
    main()
