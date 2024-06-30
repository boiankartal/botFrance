from app.database.models import async_session
from app.database.models import User, Cours
from sqlalchemy import select


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
    # try:
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
                online_or_record=data["online_or_record"],
            )
        )
        await session.commit()
        return 200


# except:
# return 500


async def get_cours(id):
    async with async_session() as session:
        return await session.scalar(select(Cours).where(Cours.id == id))
