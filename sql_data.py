import var


def create_insert_sql(table, column, value):
    query = []
    for v in value:
        insert_sql = f"INSERT INTO {table}({column}) VALUES ({v});\n"
        query.append(insert_sql)

    return query


def crate_data_sql_file(category_product, product_detail):
    queries = []

    f = open('data.sql', 'w')

    # 카테고리 삽입 쿼리 생성
    queries.append(create_insert_sql("category", var.category_cols, var.category_values))

    # 상품 삽입 쿼리
    for c in var.product_categories:
        products = category_product[c]
        queries.append(create_insert_sql("product", var.product_tb_cols, products))

    queries.append(create_insert_sql("product_detail", var.product_detail_tb_cols, product_detail))

    query_str = ""
    for query in queries:
        for q in query:
            query_str += q
        query_str += "\n"

    f.write(query_str)
    f.close()

    print(queries)
