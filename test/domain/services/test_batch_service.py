import datetime
from domain.exceptions.not_found_exception import NotFoundException
from domain.service.batch_service import BatchService
from domain.schemas.order import Order
from domain.schemas.batch import Batch
from repositories.in_memory.batches import InMemoryBatches
from repositories.in_memory.orders import InMemoryOrders
from config import settings

import pytest

@pytest.fixture
def batch_service():
	service = BatchService(batch_repository=InMemoryBatches(), order_repository=InMemoryOrders())
	return service

def test_consume(batch_service):
	consumed_before = batch_service.get_batch_by_id(settings.examples.batch_code).consumed

	now = datetime.datetime.now()
	order = Order(qty=100,
			    order_id="order id formatting is a concern of the api and database i think, domain only cares if it's unique", 
				order_id_date=now,
				batch_id=None,
				batch_code_date=now - datetime.timedelta(days=1))
	
	order2 = batch_service.consume(batch_id=settings.examples.batch_code, order= order)
	consumed_then = batch_service.get_batch_by_id(settings.examples.batch_code).consumed

	assert order2.batch_code == settings.examples.batch_code
	assert order2.qty == order.qty
	assert consumed_then - consumed_before == order.qty

def test_delete_batch_by_id(batch_service):
	deleted_at = batch_service.get_batch_by_id(settings.examples.batch_code_to_delete_during_tests).deleted_at
	assert deleted_at == None
	batch_service.delete_batch_by_id(settings.examples.batch_code_to_delete_during_tests)
	deleted_at = batch_service.get_batch_by_id(settings.examples.batch_code_to_delete_during_tests).deleted_at
	assert deleted_at != None

def test_get_active_batches(batch_service):
	batches = batch_service.get_active_batches()
	verification = [b.deleted_at == None and b.consumed < b.volume_liters and b.expiry_date > datetime.datetime.now() for b in batches]
	assert all(verification)
	assert len(batches) > 0

def test_get_batch_by_id(batch_service):
	batch = batch_service.get_batch_by_id(settings.examples.batch_code)
	assert batch.batch_code == settings.examples.batch_code

def test_get_near_expiry(batch_service):
	now = datetime.datetime.now()
	formatted_now = now.strftime(settings.datetime_string_formats.batch_code)
	batch_code = settings.examples.batch_code_to_test_near_expiry.replace("%now", formatted_now)
	batch = Batch(
		batch_code=batch_code,
		received_at=now,
		volume_liters=settings.examples.volume_liters,
		fat_percent=settings.examples.fat_percent,
		shelf_life_days=datetime.timedelta(days=settings.examples.shelf_life_days),
	)
	batch_service.post_batch(batch)
	batches = batch_service.get_near_expiry(n_days=settings.examples.shelf_life_days+1)
	assert any([b.batch_code == batch_code for b in batches])
	batches = batch_service.get_near_expiry(n_days=settings.examples.shelf_life_days-1)
	assert not any([b.batch_code == batch_code for b in batches])

def test_post_batch(batch_service):
	now = datetime.datetime.now()
	formatted_now = now.strftime(settings.datetime_string_formats.batch_code)
	batch_code = settings.examples.batch_code_to_create_during_tests.replace("%now", formatted_now)
	try:
		batch_service.get_batch_by_id(batch_code)
	except NotFoundException as e:
		assert e != None

	batch = batch_service.get_batch_by_id(settings.examples.batch_code)
	batch.batch_code = batch_code
	batch = batch_service.post_batch(batch)

	batch = batch_service.get_batch_by_id(batch_code)
	assert batch != None
