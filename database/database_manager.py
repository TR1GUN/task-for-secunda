from asyncio import current_task
import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)


class DatabaseManager:
    """Database manager"""
    # TODO: Завернуть в посгрю в контейнере, пока пускай будет локальной
    _database_path: str = f'sqlite+aiosqlite:///' + os.path.join(os.path.dirname(__file__), 'local_database.db')
    _debug: bool = True

    def __init__(self):
        self.engine = create_async_engine(
            self._database_path,
            echo=self._debug
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False, autoflush=False, expire_on_commit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()
