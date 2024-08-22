import asyncio
import os
from nio import (AsyncClient, LoginResponse, RoomMessageText, MegolmEvent)

# Konfigurace
homeserver = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
username = "xxxxxxxxxxxxxxxxxxxxxxxxx"
password = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
room_id_uber = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
device_name = "Bot Device"

# Cesta k souboru s klíči
store_path = "matrix_bot_store/"

async def send_encrypted_message(client, room_id, message):
    content = {
        "msgtype": "m.text",
        "body": message
    }
    await client.room_send(
        room_id=room_id,
        message_type="m.room.encrypted",
        content=content
    )

async def main():
    client = AsyncClient(homeserver, username, device_id=device_name, store_path=store_path)

    # Přihlášení
    response = await client.login(password, device_name=device_name)
    if isinstance(response, LoginResponse):
        print("Přihlášení úspěšné.")
    else:
        print(f"Přihlášení selhalo: {response}")
        return

    # Stažení šifrovacích klíčů
    await client.sync(full_state=True)
    await client.keys_query()
    await client.keys_upload()

    # Povolení šifrování v místnosti
    room = client.rooms[room_id_uber]
    await client.room_upgrade(room.room_id, new_version="9")

    # Povolení šifrování v místnosti
    await client.room_send(
        room_id=room_id_uber,
        message_type="m.room.encryption",
        content={
            "algorithm": "m.megolm.v1.aes-sha2"
        }
    )

    # Odeslání šifrované zprávy
    message = "Toto je šifrovaná testovací zpráva."
    await send_encrypted_message(client, room_id_uber, message)

    # Odhlášení
    await client.logout()
    await client.close()

if __name__ == "__main__":
    # Vytvoření adresáře pro ukládání šifrovacích klíčů, pokud neexistuje
    os.makedirs(store_path, exist_ok=True)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
