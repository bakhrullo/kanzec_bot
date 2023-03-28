import aiohttp


async def create_user(user_id, user_name, user_phone, config):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}user/create/",
                                data={"tg_id": user_id, "name": user_name,
                                      "phone": user_phone}) as response:
            return await response.json()


async def get_user(user_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}user/get/{user_id}") as response:
            return await response.json()


async def get_category(config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}category/") as response:
            return await response.json()


async def get_prod(cat_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}product/", params={"cat_id": cat_id}) as response:
            return await response.json()


async def get_one_prod(cat_id, config):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}product/{cat_id}") as response:
            return await response.json()


async def create_order(config, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=f"{config.db.database_url}order/create/", data={"user_id": kwargs["user_id"],
                                                                                    "product_id": kwargs["product_id"]
                                                                                    }) as response:
            return await response.json()


async def get_order(config, tg_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}order/get/", params={"tg_id": tg_id}) as response:
            return await response.json()


async def get_video(config, vd_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=f"{config.db.database_url}video/{vd_id}") as response:
            return await response.json()

