import azure.functions as func
import logging
import json
import base64
import tempfile
import os

from unstructured.partition.auto import partition

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, ContentFormat, AnalyzeResult

from .utils import extractTextWithDocumentIntelligence


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="analyzeImages", methods=['POST', 'GET'])
def analyzeImages(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Analyze Document started ...')

    if req.method == 'POST':
        try:
            data = req.get_json()
            image_data = data.get('images')
        except ValueError:
            return func.HttpResponse("Invalid JSON", status_code=400)
    elif req.method == 'GET':
        image_data = req.params.get('images')
    else:
        return func.HttpResponse("Unsupported method", status_code=405)

    if not image_data:
        return func.HttpResponse("Image data not provided", status_code=400)

    # assert image_data is a list of strings
    if not isinstance(image_data, list):
        return func.HttpResponse("Invalid image data", status_code=400)

    result = []

    for i in image_data:
        if not isinstance(i, str):
            return func.HttpResponse("Invalid image data", status_code=400)

        try:
            # Decode the base64 string
            image_bytes = base64.b64decode(i.split(',')[1])
        except Exception as e:
            logging.error(f"Error decoding base64 image: {e}")
            return func.HttpResponse("Invalid image data", status_code=400)

        try:
            # Save image_bytes to a temporary JPEG file
            with tempfile.NamedTemporaryFile(suffix=".jpeg", delete=False) as temp_file:
                temp_file.write(image_bytes)
                temp_file_path = temp_file.name

            # Process the image file as needed
            useUnstructured = True
            if useUnstructured:
                # see: https://docs.unstructured.io/open-source/introduction/overview
                elements = partition(filename=temp_file_path,
                                    content_type="image/jpeg")
                # Example processing step
                result.append({
                    "status": "success",
                    "ocr": "unstructured.io",
                    "parsed": "\n\n".join([str(el) for el in elements])
                })
            else:
                elements = extractTextWithDocumentIntelligence(temp_file_path)
                # Example processing step
                result.append({
                    "status": "success",
                    "ocr": "azure document intelligence",
                    "parsed": "\n\n".join([str(el) for el in elements])
                })

        except Exception as e:
            logging.error(f"Error processing image file: {e}")
            return func.HttpResponse("Error processing image file", status_code=500)

        finally:
            # Clean up the temporary file
            if temp_file_path:
                os.remove(temp_file_path)

    return func.HttpResponse(json.dumps({"result": result}), status_code=200)
