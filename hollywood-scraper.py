from lxml import etree
from io import StringIO, BytesIO
import requests

parser = etree.HTMLParser()
page = requests.get('http://hollywoodtheatre.org/wp-admin/admin-ajax.php?action=aec_ajax&aec_type=widget&aec_widget_id=aec_widget-5-container&aec_month=7&aec_year=2016')
events = tree.xpath('/html/body/table/tbody/tr[4]/td[4]/div')

result = etree.tostring(tree.getroot(), pretty_print=True, method="html")

print(result)
