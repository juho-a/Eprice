import asyncpg

class UserRepository:
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def get_user_by_email(self, email: str):
        conn = await asyncpg.connect(self.database_url)
        user = await conn.fetchrow("SELECT * FROM users WHERE email = $1", email)
        await conn.close()
        return user

    async def create_user(self, email: str, password_hash: str, verification_code: str):
        conn = await asyncpg.connect(self.database_url)
        try:
            await conn.execute(
                "INSERT INTO users (email, password_hash, verification_code) VALUES ($1, $2, $3)",
                email, password_hash, verification_code
            )
        finally:
            await conn.close()

    async def verify_code(self, email: str, verification_code: str):
        conn = await asyncpg.connect(self.database_url)
        try:
            result = await conn.execute(
                "UPDATE users SET is_verified = TRUE WHERE email = $1 AND verification_code = $2",
                email, verification_code
            )
            return result
        finally:
            await conn.close()

    async def update_code(self, email: str, new_code: str):
        conn = await asyncpg.connect(self.database_url)
        try:
            await conn.execute(
                "UPDATE users SET verification_code = $1 WHERE email = $2",
                new_code, email
            )
        finally:
            await conn.close()
