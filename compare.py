import boto3

KEY_SOURCE = "/home/kiaria/Downloads/source.jpeg"
KEY_TARGET = "/home/kiaria/Downloads/target.jpeg"


def compare_faces(source, target):
    client = boto3.client('rekognition')
    imageSource = open(source, 'rb')
    imageTarget = open(target, 'rb')

    response = client.compare_faces(SimilarityThreshold=80,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        confidence = str(faceMatch['Face']['Confidence'])
        print('The face matches with ' + confidence + '% confidence')

    imageSource.close()
    imageTarget.close()
    return response['FaceMatches']


def main():
    face_matches = compare_faces(KEY_SOURCE, KEY_TARGET)


if __name__ == "__main__":
    main()
