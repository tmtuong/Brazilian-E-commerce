select o.order_id, o.order_status, o.order_purchase_timestamp,
datediff(day,o.order_purchase_timestamp,o.order_approved_at) as 'aproved_after', 
datediff(day, o.order_approved_at, o.order_delivered_carrier_date) as 'carrier_take_after',
datediff(day, o.order_delivered_carrier_date, o.order_delivered_customer_date) as 'delivered_after',
datediff(day, o.order_purchase_timestamp, o.order_delivered_customer_date) as 'total_delivery_time',
datediff(day, o.order_purchase_timestamp, o.order_estimated_delivery_date) as 'estimated_delivery_time'
from orders o
