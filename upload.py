from utils import *

s3_link_prefix = 'https://s3-' + REGION + '.amazonaws.com/' + BUCKET_NAME + '/'

def upload_photos(df):
    s3_links = []

    for file_name, local_file_path in zip(df['PictureFileName'], df['LocalPictureFileName']):
        if isinstance(local_file_path, str): 
            try:
                s3.upload_file(local_file_path, BUCKET_NAME, file_name, ExtraArgs={'ContentType': "image/jpg", 'ACL': "public-read"})
                s3_links.append(s3_link_prefix + file_name)

            except Exception as e:
                s3_links.append(None)
                print(e)
        else:
            s3_links.append(None)

    return s3_links

if __name__ == "__main__":
    # read in excel file and convert to data frame
    excel_file = sys.argv[1]
    xl = pd.ExcelFile(excel_file)
    df = xl.parse('Sheet1')

    # uplaod photos and return links
    s3_links = upload_photos(df)

    # construct new excel file
    df['LinkPictureNew'] = s3_links

    output_excel_file = excel_file.replace('_upload_ready.xlsx', '_api_ready.xlsx') 
    df.to_excel(output_excel_file)