from rq import Queue
from redis import StrictRedis

r = StrictRedis.from_url('redis://localhost:28034/0')
q = Queue(connection=r)
