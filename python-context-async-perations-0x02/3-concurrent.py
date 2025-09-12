import aiosqlite
import asyncio

# Async function to fetch all users
async def async_fetch_users():
    async with aiosqlite("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursot.fetchall()
            print("ALL users:", users)
            return users

#Async function to fetch users older than 40
async async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("users older than 40", older_users)
            return older_users

# Function to run both queries concurrently
async def fetch_consurrently():
    await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users()
            )

# Run the main async function
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
