with raw as
(
	select t1.order_id, t3.customer_unique_id, t2.order_purchase_timestamp, (t1.freight_value+t1.price) as 'total_value'
	from order_items t1 
	left join orders t2 on t1.order_id = t2.order_id
	left join customer t3 on t2.customer_id = t3.customer_id
	where t2.order_status = 'delivered'
)
,
first_purchase as 
(
	select r.customer_unique_id, min(r.order_purchase_timestamp) as first_purchase_date
	from raw r
	group by r.customer_unique_id
)
,
final as
(
	select r.customer_unique_id, r.order_purchase_timestamp, f.first_purchase_date, datediff(month, f.first_purchase_date, r.order_purchase_timestamp) as date_diff
	from raw r left join first_purchase f on r.customer_unique_id = f.customer_unique_id
)
select f.date_diff ,count(distinct f.customer_unique_id) as 'customer_count', month(f.first_purchase_date) as 'month', year(f.first_purchase_date) as 'year'
from final f
group by f.date_diff, month(f.first_purchase_date), year(f.first_purchase_date)