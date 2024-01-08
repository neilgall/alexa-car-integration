import asyncio
import time
from shadow import connect_iot, change_shadow_value
from car_iot import enable_heater, get_heater_state


def callback(state: str):
    asyncio.run(enable_heater(state == "on"))


async def update():
    state = await get_heater_state()
    change_shadow_value("on" if state else "off")
    print(f"Updated shadow state: {state}")


if __name__ == "__main__":
    connect_iot(callback)

    while True:
        asyncio.run(update())
        time.sleep(1800)
