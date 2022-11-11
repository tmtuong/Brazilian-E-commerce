with raw as
(
	select t2.customer_id, t2.order_id, (t1.price+t1.freight_value) as 'total_value', t2.order_purchase_timestamp
	from order_items t1
	inner join orders t2 on t1.order_id = t2.order_id
	where t2.order_status = 'delivered'
)

select c.customer_unique_id, r.order_id, r.total_value, r.order_purchase_timestamp
from raw r inner join customer c on r.customer_id = c.customer_id