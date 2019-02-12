import datetime
import os

import boto3
import dateutil.parser
import dateutil.tz
import xlsxwriter


def push_to_s3(file_path, title, bucket="slow.query.logs"):
    s3 = boto3.resource('s3')
    time_stamp = datetime.datetime.now().strftime('%s')
    s3.Bucket(bucket).upload_file(file_path, "%s/report-%s.xlsx" % (title, time_stamp))
    bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location['LocationConstraint'], bucket,
                                                               "%s/report-%s.xlsx" % (title, time_stamp))
    os.remove("%s_report.xlsx" % (title))
    return object_url


def report_generate(list_of_print, timelapse, title="mongo", bucket="slow.query.logs"):
    """

    :param list_of_print:
    :param timelapse:
    :param title:
    :param bucket:
    :return:
    """
    heads = tuple(list_of_print[0].keys())
    current_time = datetime.datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc())
    parse_ignore_timestamp = current_time - datetime.timedelta(hours=timelapse)
    complete_path = os.path.join(os.getcwd(), "%s_report.xlsx" % title)

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(complete_path)
    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': 'black', 'locked': True})

    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'yellow'})

    worksheet.merge_range('A1:%s2' % chr(ord("A") + len(heads) - 1), 'LimeTray %s Report' % title.capitalize(),
                          merge_format)

    # Add a bold format to use to highlight cells.
    normal_query_wrap = workbook.add_format({'text_wrap': True})
    start_time_column = int(len(heads) / 2) - 1
    worksheet.merge_range('A3:%s3' % chr(ord("A") + start_time_column), 'Start Time', merge_format)
    worksheet.merge_range('%s3:%s3' % (chr(ord("A") + start_time_column + 1), chr(ord("A") + len(heads) - 1)),
                          parse_ignore_timestamp.strftime("%Y-%m-%d %H:%M"), merge_format)

    worksheet.merge_range('A4:%s4' % chr(ord("A") + start_time_column), 'End Time', merge_format)
    worksheet.merge_range('%s4:%s4' % (chr(ord("A") + start_time_column + 1), chr(ord("A") + len(heads) - 1)),
                          current_time.strftime("%Y-%m-%d %H:%M"), merge_format)
    # Titles

    column = "A"
    for head in heads:
        worksheet.write('%s5' % column, head, bold)
        column = chr(ord(column) + 1)

    # Write some numbers, with row/column notation.
    column_start = 5
    for element in list_of_print:
        for count in range(len(heads)):
            try:
                if isinstance(element[heads[count]], str):
                    unicode_query = ''.join([i if ord(i) < 128 else ' ' for i in element[heads[count]]])
                else:
                    unicode_query = element[heads[count]]
                worksheet.write(column_start, count, unicode_query)

            except Exception as e:
                print(e)
                raise
        column_start += 1

    workbook.close()
    resp = push_to_s3("%s_report.xlsx" % title, title, bucket)
    return resp
