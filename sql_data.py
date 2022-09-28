import var

def create_category_insert_sql():
    query = []
    for c in var.product_categories:
        insert_sql = f"INSERT INTO category (name) VALUES ('{c}')"
        query.append(insert_sql)

    return query


def create_product_insert_sql(category_product):
    query = []
    category_id = 1
    for c in var.product_categories:
        products = category_product[c]

        for p in products:
            insert_sql = f"INSERT INTO product ({var.product_tb_cols}) VALUES ({category_id}, {p})"
            query.append(insert_sql)

        category_id += 1

    return query


def crate_data_sql_file(category_product):
    queries = [create_category_insert_sql(), create_product_insert_sql(category_product)]

    f = open('data.sql', 'w')

    query_str = ""
    for query in queries:
        for q in query:
            query_str += q + "\n"
        query_str += "\n\n"

    f.write(query_str)
    f.close()

    print(queries)

    # return queries


