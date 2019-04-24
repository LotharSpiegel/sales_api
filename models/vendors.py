from flask import g
from flask_restplus import fields

from sales_api.models.base import BaseModel

class VendorProductInfo:
	def __init__(self, vendor, WholesalePrice, DaysToDeliver):
		self.vendor = vendor
		self.WholesalePrice = WholesalePrice
		self.DaysToDeliver = DaysToDeliver

	@classmethod
	def _instance_factory(cls, row):
		vendor_row = row[:-2]
		vendor = Vendor._instance_factory(vendor_row)
		return cls(vendor=vendor, WholesalePrice=row[-2], DaysToDeliver=row[-1])

	def as_dict(self):
		d = {}
		d.update(self.vendor.as_dict())
		d['WholesalePrice'] = float(self.WholesalePrice)
		d['DaysToDeliver'] = int(self.DaysToDeliver)
		return d

class Vendor(BaseModel):
	table_name = 'vendors'
	columns = ['VendorId', 'VendName', 'VendStreetAddress', 'VendCity',
			'VendState', 'VendZipCode', 'VendPhoneNumber', 'VendFaxNumber',
			'VendWebPage', 'VendEmailAddress']
	nice_columns = ['VendorId', 'Name', 'StreetAddress', 'City',
			'State', 'ZipCode', 'PhoneNumber', 'FaxNumber',
			'WebPage', 'EmailAddress']
	column_types = [int, str, str, str,
			str, str, str, str,
			str, str]
	id_column = 'VendorId'

class ProductVendor(BaseModel):
	"""An m2m junction table between proucts(ProductNumber) and vendors(VendorId)"""
	table_name = 'product_vendors'
	columns = ['ProductNumber', 'VendorId', 'WholesalePrice', 'DaysToDeliver']
	nice_columns = ['ProductNumber', 'VendorId', 'WholesalePrice', 'DaysToDeliver']
	column_types = [int, int, float, int]
	id_column = None