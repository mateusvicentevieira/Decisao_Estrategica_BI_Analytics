"""Garante que compatibilidade não seja confundida com schema nativo validado."""
import unittest
import requests
from validate_pbip import validate_document

PUBLIC='https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.5.0/schema.json'
NATIVE=PUBLIC.replace('2.5.0','2.14.0')
SCHEMA={'type':'object','properties':{'$schema':{'const':PUBLIC},'name':{'type':'string'}},'required':['$schema','name'],'additionalProperties':False}

def loader(url):
    if url==PUBLIC:return SCHEMA
    response=requests.Response();response.status_code=404;response.url=url
    raise requests.HTTPError('Schema indisponível',response=response)

class CompatibilityTests(unittest.TestCase):
    def test_public_schema_is_distinguished_from_compatibility(self):
        result=validate_document({'$schema':PUBLIC,'name':'visual'},loader)
        self.assertEqual(result['mode'],'declared')
        result=validate_document({'$schema':NATIVE,'name':'visual'},loader)
        self.assertEqual(result['mode'],'compatibility')
        self.assertEqual(result['validated_schema'],PUBLIC)

    def test_fallback_checks_all_properties_and_preserves_native_document(self):
        document={'$schema':NATIVE,'name':'visual','unknown':42}
        result=validate_document(document,loader)
        self.assertTrue(result['errors'])
        self.assertEqual(document,{'$schema':NATIVE,'name':'visual','unknown':42})

    def test_strict_mode_keeps_failure_for_unpublished_schema(self):
        with self.assertRaises(requests.HTTPError):
            validate_document({'$schema':NATIVE,'name':'visual'},loader,allow_compatibility=False)

    def test_unknown_versions_are_not_automatically_downgraded(self):
        with self.assertRaises(requests.HTTPError):
            validate_document({'$schema':NATIVE.replace('2.14.0','99.0.0'),'name':'visual'},loader)

if __name__=='__main__':unittest.main()
