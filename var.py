
product_categories = ["신상품", "닭가슴살", "도시락·볶음밥", "샐러드·과일", "즉석 간편식", "음료·차·프로틴", "계란·난백·콩", "소고기"]
# product_categories = ["음료·차·프로틴"]

category_values = ["'신상품'", "'닭가슴살'", "'도시락·볶음밥'", "'샐러드·과일'", "'즉석 간편식'", "'음료·차·프로틴'", "'계란·난백·콩'", "'소고기'"]
# category_values = ["'음료·차·프로틴'"]


category_cols = "name"
product_tb_cols = "category_id, price, name, display_name, stock, deadline, thumbnail, seller_id," \
                  " delivery_fee, created_date, last_modified_date"
product_detail_tb_cols = "product_id, orders, image, created_date, last_modified_date"
