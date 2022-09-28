import ranking_dak
import sql_data


if __name__ == '__main__':
    category_product = ranking_dak.scrap()
    print(category_product)

    query = sql_data.crate_data_sql_file(category_product)
    print(query)

