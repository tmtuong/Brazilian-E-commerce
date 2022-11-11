select o.order_id, o.product_id,o.order_item_id, p1.product_category_name_english, ord.order_purchase_timestamp
from order_items o 
left join products p on o.product_id = p.product_id
left join product_category_name_translation p1 on p.product_category_name = p1.product_category_name
left join orders ord on o.order_id = ord.order_id