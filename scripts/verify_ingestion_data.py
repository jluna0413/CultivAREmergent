import asyncio
from sqlalchemy import select
from app.models_async.base import AsyncSessionLocal
from app.models_async.grow import Breeder, Cultivar

async def verify_data():
    async with AsyncSessionLocal() as session:
        # Check Breeder
        breeder_result = await session.execute(select(Breeder).where(Breeder.name == "Barney's Farm"))
        breeder = breeder_result.scalar_one_or_none()
        if breeder:
            print(f"Breeder Found: {breeder.name} (ID: {breeder.id}, SF ID: {breeder.seedfinder_id})")
        else:
            print("Breeder 'Barney's Farm' not found.")

        # Check Cultivar
        cultivar_result = await session.execute(select(Cultivar).where(Cultivar.name == "Blueberry Zkittlez"))
        cultivar = cultivar_result.scalar_one_or_none()
        if cultivar:
            print(f"Cultivar Found: {cultivar.name} (ID: {cultivar.id}, Breeder ID: {cultivar.breeder_id})")
            print(f"Lineage: {cultivar.lineage_json}")
            print(f"Images: {cultivar.image_urls}")
        else:
            print("Cultivar 'Blueberry Zkittlez' not found.")

if __name__ == "__main__":
    asyncio.run(verify_data())
