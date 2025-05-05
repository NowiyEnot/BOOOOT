import aiosqlite

__all__ = [
    'db_start',
    'create_item',
    'get_items_by_category',
    'get_item_by_id',
    'delete_item',
    'add_item_to_cart',
    'get_cart_items',
    'delete_item_from_cart',
    'clear_cart',
    'update_item'  # Добавлена в список экспортируемых функций
]


async def db_start():
    async with aiosqlite.connect('tg.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS accounts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            tg_id INTEGER,
                            cart_id TEXT
                            )""")
        await db.commit()

        await db.execute("""CREATE TABLE IF NOT EXISTS items (
                            i_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            desc TEXT,
                            price TEXT,
                            photo TEXT,
                            brand TEXT
                            )""")
        await db.commit()

        await db.execute("""CREATE TABLE IF NOT EXISTS cart (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            item_id INTEGER,
                            quantity INTEGER DEFAULT 1
                            )""")
        await db.commit()

        # Обновление структуры таблицы cart, если столбец quantity отсутствует
        try:
            await db.execute("ALTER TABLE cart ADD COLUMN quantity INTEGER DEFAULT 1")
            await db.commit()
        except aiosqlite.OperationalError:
            # Колонка уже существует, игнорируем ошибку
            pass


class Item:
    def __init__(self, id, name, desc, price, photo):
        self.id = id
        self.name = name
        self.desc = desc
        self.price = price
        self.photo = photo


async def create_item(name, desc, price, photo, brand):
    async with aiosqlite.connect('tg.db') as db:
        await db.execute("""INSERT INTO items (name, desc, price, photo, brand)
                            VALUES (?, ?, ?, ?, ?)""",
                         (name, desc, price, photo, brand))
        await db.commit()


async def get_items_by_category(category):
    async with aiosqlite.connect('tg.db') as db:
        cursor = await db.execute("SELECT * FROM items WHERE brand = ?", (category,))
        rows = await cursor.fetchall()
        items = [Item(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        return items


async def get_item_by_id(item_id):
    async with aiosqlite.connect('tg.db') as db:
        cursor = await db.execute("SELECT * FROM items WHERE i_id = ?", (item_id,))
        row = await cursor.fetchone()
        if row:
            return Item(row[0], row[1], row[2], row[3], row[4])
        return None


async def delete_item(item_name):
    async with aiosqlite.connect('tg.db') as db:
        await db.execute("DELETE FROM items WHERE name = ?", (item_name,))
        await db.commit()
        return True


async def add_item_to_cart(user_id, item_id):
    async with aiosqlite.connect('tg.db') as db:
        cursor = await db.execute("SELECT * FROM cart WHERE user_id = ? AND item_id = ?", (user_id, item_id))
        cart_item = await cursor.fetchone()
        if cart_item:
            await db.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND item_id = ?",
                             (user_id, item_id))
        else:
            await db.execute("INSERT INTO cart (user_id, item_id, quantity) VALUES (?, ?, 1)",
                             (user_id, item_id))
        await db.commit()
        return True


async def get_cart_items(user_id):
    async with aiosqlite.connect('tg.db') as db:
        items = []
        cursor = await db.execute("""
            SELECT items.i_id, items.name, items.price, cart.quantity 
            FROM cart 
            INNER JOIN items ON cart.item_id = items.i_id 
            WHERE cart.user_id = ?
        """, (user_id,))
        async for row in cursor:
            item_id, item_name, item_price, quantity = row
            items.append((Item(item_id, item_name, "", item_price, ""), quantity))
        return items


async def delete_item_from_cart(user_id, item_id):
    async with aiosqlite.connect('tg.db') as db:
        cursor = await db.execute("SELECT quantity FROM cart WHERE user_id = ? AND item_id = ?",
                                  (user_id, item_id))
        cart_item = await cursor.fetchone()
        if cart_item and cart_item[0] > 1:
            await db.execute("UPDATE cart SET quantity = quantity - 1 WHERE user_id = ? AND item_id = ?",
                             (user_id, item_id))
        else:
            await db.execute("DELETE FROM cart WHERE user_id = ? AND item_id = ?",
                             (user_id, item_id))
        await db.commit()
        return True


async def clear_cart(user_id):
    async with aiosqlite.connect('tg.db') as db:
        await db.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        await db.commit()


async def update_item(item_name, **kwargs):
    """Обновляет данные товара в базе данных"""
    valid_fields = {'name', 'desc', 'price', 'photo', 'brand'}
    update_data = {k: v for k, v in kwargs.items() if k in valid_fields}

    if not update_data:
        return False

    async with aiosqlite.connect('tg.db') as db:
        # Проверяем существование товара
        cursor = await db.execute("SELECT 1 FROM items WHERE name = ?", (item_name,))
        if not await cursor.fetchone():
            return False

        # Формируем SQL запрос
        set_clause = ", ".join([f"{field} = ?" for field in update_data])
        values = list(update_data.values())
        values.append(item_name)

        await db.execute(
            f"UPDATE items SET {set_clause} WHERE name = ?",
            values
        )
        await db.commit()
        return True