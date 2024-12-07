import asyncio
from datetime import datetime
from logger import logger


async def find_optimal_parallelism(client, files, max_uploads_range, upload_func):
    """Подбирает оптимальное количество параллельных загрузок."""
    optimal_parallelism = max_uploads_range[0]
    best_time = float('inf')

    for parallelism in range(max_uploads_range[0], max_uploads_range[1] + 1):
        logger.info(f"Тестирование с {parallelism} параллельными загрузками...")
        start_time = datetime.now()

        semaphore = asyncio.Semaphore(parallelism)

        async def upload_file(file_path):
            async with semaphore:
                await upload_func(client, file_path)

        tasks = [upload_file(file_path) for file_path in files]
        await asyncio.gather(*tasks)

        elapsed_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"Время загрузки с {parallelism} параллельными задачами: {elapsed_time:.2f} секунд.")

        if elapsed_time < best_time:
            best_time = elapsed_time
            optimal_parallelism = parallelism

    logger.info(f"Оптимальное количество параллельных загрузок: {optimal_parallelism}")
    return optimal_parallelism
