# app/db/base.py

# Import all the models, so that Base has them before being imported by Alembic
from app.models.facility import Facility
from app.models.inventory import Inventory
from app.models.requisition import Requisition
from app.models.medication import Medication
from app.models.transfer import Transfer
from app.models.purchase_order import PurchaseOrder
from app.models.vendor import Vendor
from app.models.user import User

from app.db.base_class import Base  # Import the Base class

# Ensure that all models are imported and registered with the Base class
