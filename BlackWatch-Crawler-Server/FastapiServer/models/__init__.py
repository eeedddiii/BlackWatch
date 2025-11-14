import logging
from pymongo import AsyncMongoClient
from pymongo.errors import ConnectionFailure
from config import config

# 로거 설정
logger = logging.getLogger('main')

class MongoDB:
    mongo_url = config.MONGO_URL
    mongo_db = config.MONGO_DB_NAME

    client: AsyncMongoClient | None = None
    db = None

    @classmethod
    async def connect(cls):
        # 데이터베이스에 연결
        logger.info("Connecting to MongoDB...")
        try:
            cls.client = AsyncMongoClient(cls.mongo_url)
            # 서버 정보 요청을 통해 실제 연결을 확인
            await cls.client.admin.command('ping')
            cls.db = cls.client[cls.mongo_db]
            logger.info("Successfully connected to MongoDB.")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    @classmethod
    async def close(cls):
        # 데이터베이스 닫기
        if cls.client:
            await cls.client.close()
            logger.info("MongoDB connection closed.")


# 애플리케이션 전역에서 사용할 인스턴스
mongodb = MongoDB()