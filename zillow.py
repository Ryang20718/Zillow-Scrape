from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

address = '1267 via caliente'
zipcode = '92069'

zillow_data = ZillowWrapper('X1-ZWz187irghgpaj_17jma')
deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
result = GetDeepSearchResults(deep_search_response)

print(result.bathrooms) 