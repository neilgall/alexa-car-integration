from aiohttp import ClientSession
from renault_api.renault_client import RenaultClient
from renault_api.renault_vehicle import RenaultVehicle
import logging
import os

USERNAME = os.environ["RENAULT_USERNAME"]
PASSWORD = os.environ["RENAULT_PASSWORD"]
REGISTRATION = os.environ["RENAULT_REGISTRATION"]

async def get_heater_state() -> bool:
    async with ClientSession() as websession:
        try:
            car = await renault_login(websession)
            hvac = await car.get_hvac_status()
            return hvac.hvacStatus == "on"
        
        except Exception as e:
            logging.error("failed to get heater state", e)
            return false


async def enable_heater(state: bool):
    async with ClientSession() as websession:
        try:
            car = await renault_login(websession)
            if state:
                rsp = await car.set_ac_start(temperature=19)
            else:
                rsp = await car.set_ac_stop()
            print(f"enable_heater({state}) -> {rsp}")
        
        except Exception as e:
            logging.error("failed to set heater state", e)


async def renault_login(websession: ClientSession) -> RenaultVehicle:
    client = RenaultClient(websession=websession, locale="en_GB")
    await client.session.login(USERNAME, PASSWORD)
    person = await client.get_person()
    account_id = next(
        account.accountId
        for account in person.accounts
        if account.accountType == "MYRENAULT"
    )
    account = await client.get_api_account(account_id)
    vehicles = await account.get_vehicles()
    vin = next(
        vehicle.vin
        for vehicle in vehicles.vehicleLinks
        if vehicle.vehicleDetails.registrationNumber == REGISTRATION
    )
    return await account.get_api_vehicle(vin)
