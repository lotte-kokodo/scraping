import ranking_dak
import sql_data


if __name__ == '__main__':
    category_product, product_detail = ranking_dak.scrap()
    print(category_product)

    sql_data.crate_data_sql_file(category_product, product_detail)

