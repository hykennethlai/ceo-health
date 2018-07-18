from utils import *

def save_image_from_url(url, image_file_name):
    response = request.Request(url, headers={'User-Agent': 'Magic Browser'})
    content = request.urlopen(response).read()
    with open(image_file_name, 'wb') as f:
        f.write(request.urlopen(response).read())

def microsoft_return_face_data(url):
    if isinstance(url, str):
        data = {'url': url}
        response = requests.post(FACE_API_URL, params=params, headers=headers, json=data)
        faces = response.json()
    return faces

def download_pictures(df):
    multi_face = []
    picture_file_names_local = []
    picture_file_names = []

    local_folder = 'ceo_pictures/'

    prev_ceo = None

    for index, row in df.iterrows():
        company = row['Company'].lower()
        ceo = row['CEO'].lower()
        
        if ceo == prev_ceo:
            ceo_indexer += 1
        else:
            ceo_indexer = 0
        
        ceo_url = '_'.join(ceo.split(' '))
        ceo_folder_name = company + '-' + ceo_url + '/'
        image_file_name = company + '-' + ceo_url + '-' + str(ceo_indexer) + '.jpg'
        prev_ceo = ceo
        
        url = row['LinkPicture']
        
        multi_face_indicator = 0
        if type(url) is not float:
            try:
                # use face Api to check if it has multiple faces
                faces = microsoft_return_face_data(url)
                if len(faces) > 1:
                    multi_face_indicator = 1
                multi_face.append(multi_face_indicator)
            except Exception as e:
                multi_face.append(None)
                print(e)


            try:
                # save to local
                ## if not multi_face save in default folder
                if multi_face_indicator == 0:
                    directory = 'ceo_pictures/' + ceo_folder_name
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    save_image_from_url(url, directory + image_file_name)

                ## otherwise create a new folder for picture with multi-faces and store it in there
                else:
                    directory = 'ceo_pictures/' + ceo_folder_name + 'MULTI_FACE/'
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    save_image_from_url(url, directory + image_file_name)

                picture_file_names.append(image_file_name)
                picture_file_names_local.append(directory + image_file_name)

            except Exception as e:
                picture_file_names.append(None)
                picture_file_names_local.append(None)
                print(e)

        else:
            multi_face.append(None)
            picture_file_names.append(None)
            picture_file_names_local.append(None)

    return multi_face, picture_file_names, picture_file_names_local


if __name__ == "__main__":

    # read in excel file and convert to data frame
    excel_file = sys.argv[1]
    xl = pd.ExcelFile(excel_file)
    df = xl.parse('Sheet1')

    # DEBUG MODE:
    df = df[:50]

    # run the main function
    multi_face, picture_file_names, picture_file_names_local = download_pictures(df)

    # create new excel sheet
    df['Multi-face'] = multi_face
    df['PictureFileName'] = picture_file_names
    df['LocalPictureFileName'] = picture_file_names_local
    
    output_excel_file = excel_file.replace('.xlsx', '_upload_ready.xlsx') 
    df.to_excel(output_excel_file)

