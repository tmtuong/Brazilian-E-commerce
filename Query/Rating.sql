select p.review_id, pd.product_id, t.product_category_name_english, p.review_comment_title, p.review_comment_message, p.review_score
from order_previews p
left join order_items i on p.order_id = i.order_id
left join products pd on i.product_id = pd.product_id
inner join product_category_name_translation t on pd.product_category_name = t.product_category_name