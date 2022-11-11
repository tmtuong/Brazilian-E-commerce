select t1.order_id, t3.customer_unique_id, t2.order_purchase_timestamp, (t1.freight_value+t1.price) as 'total_value'
from order_items t1 
left join orders t2 on t1.order_id = t2.order_id
left join customer t3 on t2.customer_id = t3.customer_id
where t2.order_status = 'delivered'