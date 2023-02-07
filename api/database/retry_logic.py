import time
from sqlalchemy import create_engine

MAX_RETRIES = 5
RETRY_INTERVAL = 5 # in seconds

def create_engine_with_retry(db_url, max_retries=MAX_RETRIES, retry_interval=RETRY_INTERVAL):
  for retry in range(max_retries):
    try:
      return create_engine(db_url)
    except Exception as e:
      if retry == max_retries - 1:
          raise e
      time.sleep(retry_interval)
