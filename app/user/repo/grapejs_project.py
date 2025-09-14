import uuid

from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.grapejs_project import CreateProject
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.grapejs_project import GrapeJSProject
from app.utils.utils import build_base_query


async def create_or_update_project(
    db: AsyncSession,
    payload: CreateProject
) -> GrapeJSProject:
    project_id = payload.id
    db_project = await get_project_by_id(db, project_id)

    if db_project:
        db_project.data = payload.data
    else:
        db_project = GrapeJSProject(
            id=project_id,
            data=payload.data
        )
        db.add(db_project)

    try:
        await db.commit()
        await db.refresh(db_project)
    except (OperationalError, DataError):
        raise DatabaseException("Database operation failed")

    return db_project


async def get_project_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> GrapeJSProject:
    query = build_base_query(GrapeJSProject)
    query = query.filter(GrapeJSProject.id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()




