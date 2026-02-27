import asyncio

from src.infrastructure.persistence.database.connection import Base, engine


async def test():
    print("🔍 Conectando ao banco...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Conexão OK! Tabelas criadas.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test())
