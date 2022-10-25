from clients.kafka import get_faust_app
from clients.clickhouse import ClickHouseLoader
from core.config import settings, etl_logger
from models.view import View
from transform import transform_view

app = get_faust_app()
views_topic = app.topic('views', key_type=bytes, value_type=str)

ch_loader = ClickHouseLoader(dsn=settings.ch_settings.dsn)


@app.agent(views_topic)
async def on_event(stream) -> None:
    views = []
    async for msg_key, msg_value in stream.items():
        view: View = transform_view(msg_value)
        views.append(view.dict())
    await ch_loader.load_data(views)
