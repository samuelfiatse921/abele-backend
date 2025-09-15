from sqlalchemy import and_
from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.grapejs_project import CreateProject, FilterProject
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.grapejs_project import GrapeJSProject
from app.utils.utils import build_base_query, generate_uuid


async def create_or_update_project(
    db: AsyncSession,
    payload: CreateProject
) -> GrapeJSProject:
    template_id = payload.templateId
    user_id = payload.userId

    filter_project = FilterProject(user_id=user_id, template_id=template_id)
    db_project = await get_project_by_id(db, filter_project)

    if db_project:
        db_project.data = payload.data
    else:
        db_project = GrapeJSProject(
            id=generate_uuid(),
            user_id=user_id,
            template_id=template_id,
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
    request: FilterProject
) -> GrapeJSProject:
    query = build_base_query(GrapeJSProject)
    query = query.where(
        and_(
            GrapeJSProject.user_id == request.user_id,
            GrapeJSProject.template_id == request.template_id
        )
    )
    record_found = await db.execute(query)

    return record_found.scalars().first()




