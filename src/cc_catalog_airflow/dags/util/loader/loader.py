from util.loader import paths, s3, sql


def load_local_data(output_dir, postgres_conn_id, identifier):
    tsv_file_name = paths.get_staged_file(output_dir, identifier)
    sql.load_local_data_to_intermediate_table(
        postgres_conn_id,
        tsv_file_name,
        identifier
    )
    sql.upsert_records_to_image_table(postgres_conn_id, identifier)


def copy_to_s3(output_dir, bucket, identifier, aws_conn_id):
    tsv_file_name = paths.get_staged_file(output_dir, identifier)
    s3.copy_file_to_s3_staging(identifier, tsv_file_name, bucket, aws_conn_id)


def load_s3_data(
        bucket,
        aws_conn_id,
        postgres_conn_id,
        identifier
):
    tsv_key = s3.get_staged_s3_object(identifier, bucket, aws_conn_id)
    sql.load_s3_data_to_intermediate_table(
        postgres_conn_id,
        bucket,
        tsv_key,
        identifier
    )
    sql.upsert_records_to_image_table(postgres_conn_id, identifier)
