# Import the SDK
import easyapiio

if not results['success']:
    print(results['message'])  # Prints error
else:
    # Successful case

    # Sub in your API Key and App Id which can be found on EasyAPI.io
    EasyAPIFileAPI = easyapiio.File('YOUR_API_KEY', 'YOUR_APP_ID')

    # Upload your file. ./ <-- is the current folder
    results = EasyAPIFileAPI.upload(open('./my_upload_file.txt', 'rb'))

    print(results['file']['id'])

    # Deleting with the id
    EasyAPIFileAPI = easyapiio.File('YOUR_API_KEY', 'YOUR_APP_ID')
    results = EasyAPIFileAPI.delete('YOUR_FILE_ID')
