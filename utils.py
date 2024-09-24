import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient


# see: 
# Use Azure Document Intelligence
# https://docs.microsoft.com/en-us/azure/cognitive-services/document-ai/overview

AZURE_COGNITIVE_SERVICES_SUBDOMAIN = os.environ["AZURE_COGNITIVE_SERVICES_SUBDOMAIN"]
AZURE_COGNITIVE_SERVICES_API_KEY = os.environ["AZURE_COGNITIVE_SERVICES_API_KEY"]


def extractTextWithDocumentIntelligence(image_path):
    endpoint = f"https://{AZURE_COGNITIVE_SERVICES_SUBDOMAIN}.cognitiveservices.azure.com/"
    credential = AzureKeyCredential(AZURE_COGNITIVE_SERVICES_API_KEY)
    document_intelligence_client = DocumentIntelligenceClient(endpoint, credential)

