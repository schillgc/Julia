import io

from docutils.parsers.rst.directives import uri, path

'''Construct objects that represent image content'''

# From a local file
# with io.open(path, 'rb') as image_file:
#     content = image_file.read()
#
# image = vision.types.Image(content=content)

# From a URI
image = vision.types.Image()
image.source.image_uri = uri


'''Make requests and process responses'''
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.face_detection(image=image)
faces = response.face_annotations

# Names of likelihood from google.cloud.vision.enums
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                   'LIKELY', 'VERY_LIKELY')
print('Faces:')

for face in faces:
    print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
    print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
    print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in face.bounding_poly.vertices])

    print('face bounds: {}'.format(','.join(vertices)))


'''Make a landmark detection request and process the response'''
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.landmark_detection(image=image)
landmarks = response.landmark_annotations
print('Landmarks:')

for landmark in landmarks:
    print(landmark.description)
    for location in landmark.locations:
        lat_lng = location.lat_lng
        print('Latitude {}'.format(lat_lng.latitude))
        print('Longitude {}'.format(lat_lng.longitude))


'''Make a logo detection request and process the response'''
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.logo_detection(image=image)
logos = response.logo_annotations
print('Logos:')

for logo in logos:
    print(logo.description)


'''Make a safe search detection request and process the response'''
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.safe_search_detection(image=image)
safe = response.safe_search_annotation


'''Names of likelihood from google.cloud.vision.enums'''
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                   'LIKELY', 'VERY_LIKELY')
print('Safe search:')

print('adult: {}'.format(likelihood_name[safe.adult]))
print('medical: {}'.format(likelihood_name[safe.medical]))
print('spoofed: {}'.format(likelihood_name[safe.spoof]))
print('violence: {}'.format(likelihood_name[safe.violence]))
print('racy: {}'.format(likelihood_name[safe.racy]))


'''Make a text detection request and processing the response'''
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations
print('Texts:')

for text in texts:
    print('\n"{}"'.format(text.description))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in text.bounding_poly.vertices])

    print('bounds: {}'.format(','.join(vertices)))


'''Make a document text detection request and processing the response'''
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.document_text_detection(image=image)

for page in response.full_text_annotation.pages:
    for block in page.blocks:
        print('\nBlock confidence: {}\n'.format(block.confidence))

        for paragraph in block.paragraphs:
            print('Paragraph confidence: {}'.format(
                paragraph.confidence))

            for word in paragraph.words:
                word_text = ''.join([
                    symbol.text for symbol in word.symbols
                ])
                print('Word text: {} (confidence: {})'.format(
                    word_text, word.confidence))

                for symbol in word.symbols:
                    print('\tSymbol: {} (confidence: {})'.format(
                        symbol.text, symbol.confidence))


'''Making an image properties request and processing the response'''
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.image_properties(image=image)
props = response.image_properties_annotation
print('Properties:')

for color in props.dominant_colors.colors:
    print('fraction: {}'.format(color.pixel_fraction))
    print('\tr: {}'.format(color.color.red))
    print('\tg: {}'.format(color.color.green))
    print('\tb: {}'.format(color.color.blue))
    print('\ta: {}'.format(color.color.alpha))


'''Make a web detection request and processing the response'''
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.web_detection(image=image)
annotations = response.web_detection

if annotations.best_guess_labels:
    for label in annotations.best_guess_labels:
        print('\nBest guess label: {}'.format(label.label))

if annotations.pages_with_matching_images:
    print('\n{} Pages with matching images found:'.format(
        len(annotations.pages_with_matching_images)))

    for page in annotations.pages_with_matching_images:
        print('\n\tPage url   : {}'.format(page.url))

        if page.full_matching_images:
            print('\t{} Full Matches found: '.format(
                   len(page.full_matching_images)))

            for image in page.full_matching_images:
                print('\t\tImage url  : {}'.format(image.url))

        if page.partial_matching_images:
            print('\t{} Partial Matches found: '.format(
                   len(page.partial_matching_images)))

            for image in page.partial_matching_images:
                print('\t\tImage url  : {}'.format(image.url))

if annotations.web_entities:
    print('\n{} Web entities found: '.format(
        len(annotations.web_entities)))

    for entity in annotations.web_entities:
        print('\n\tScore      : {}'.format(entity.score))
        print(u'\tDescription: {}'.format(entity.description))

if annotations.visually_similar_images:
    print('\n{} visually similar images found:\n'.format(
        len(annotations.visually_similar_images)))

    for image in annotations.visually_similar_images:
        print('\tImage url    : {}'.format(image.url))


'''Make a crop hints request and processing the response'''
with io.open(path, 'rb') as image_file:
    content = image_file.read()
image = vision.types.Image(content=content)

crop_hints_params = vision.types.CropHintsParams(aspect_ratios=[1.77])
image_context = vision.types.ImageContext(
    crop_hints_params=crop_hints_params)

response = client.crop_hints(image=image, image_context=image_context)
hints = response.crop_hints_annotation.crop_hints

for n, hint in enumerate(hints):
    print('\nCrop Hint: {}'.format(n))

    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in hint.bounding_poly.vertices])

    print('bounds: {}'.format(','.join(vertices)))
