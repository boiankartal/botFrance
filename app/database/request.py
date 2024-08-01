from app.database.models import async_session
from app.database.models import User, Cours
from sqlalchemy import select, update, delete


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, cours=0))
            await session.commit()


async def get_courses():
    courses = []
    async with async_session() as session:
        for cours in await session.scalars(select(Cours)):
            if cours.active == "Да":
                courses.append(cours)
    return courses


async def get_courses_admin():
    async with async_session() as session:
        return await session.scalars(select(Cours))


async def set_new_cours(data):
    try:
        async with async_session() as session:
            courses = await session.scalars(select(Cours))
            id = 1
            number = 0
            if courses:
                for cours in courses:
                    number = number + 1
                id = number + 1
            session.add(
                Cours(
                    id=id,
                    name=data["name"],
                    description=data["description"],
                    img_tg_id=data["img_id"],
                    active=data["active"],
                    price=data["price"],
                    dates=data["dates"],
                    main=data["main"],
                    online_or_record=data["online_or_record"],
                    url=data["url"]
                )
            )
            await session.commit()
            return 200

    except:
        return 500


async def get_cours(id):
    async with async_session() as session:
        return await session.scalar(select(Cours).where(Cours.id == id))


async def editActive(id):
    async with async_session() as session:
        cours = await get_cours(id)
        if cours.active == "Да":
            status = "Нет"
        elif cours.active == "Нет":
            status = "Да"
        await session.execute(update(Cours).where(Cours.id == id).values(active=status))
        await session.commit()
        return 200


async def delete_cours(id):
    async with async_session() as session:
        try:
            await session.execute(delete(Cours).where(Cours.id == id))
            await session.commit()
            return 200
        except:
            return 500


async def editName(id, new_name):
    try:
        async with async_session() as session:
            await session.execute(
                update(Cours).where(Cours.id == id).values(name=new_name)
            )
            await session.commit()
        return 200
    except:
        return 500

async def editDates(id, new_name):
    try:
        async with async_session() as session:
            await session.execute(
                update(Cours).where(Cours.id == id).values(name=new_name)
            )
            await session.commit()
        return 200
    except:
        return 500

async def editImages(id, new_images):
    try:
        async with async_session() as session:
            await session.execute(
                update(Cours).where(Cours.id == id).values(img_tg_id=new_images)
            )
            await session.commit()
        return 200
    except:
        return 500


async def editDescription(id, new_description):
    try:
        async with async_session() as session:
            await session.execute(
                update(Cours).where(Cours.id == id).values(description=new_description)
            )
            await session.commit()
        return 200
    except:
        return 500


async def editPrice(id, new_price):
    try:
        async with async_session() as session:
            await session.execute(
                update(Cours).where(Cours.id == id).values(price=new_price)
            )
            await session.commit()
        return 200
    except:
        return 500


async def get_user(tg_id):
    try:
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))
            return user

    except:
        return 500


async def get_users():
    try:
        async with async_session() as session:
            return await session.scalars(select(User))
    except:
        return 500


async def get_url_cours(id):
    try:
        async with async_session() as session:
            cours = await session.scalar(select(Cours).where(Cours.id == id))
            return cours
    except:
        return 500