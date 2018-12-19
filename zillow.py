from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

address = 'address goes here'
zipcode = 'zip goes here'

zillow_data = ZillowWrapper('api token')
deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
result = GetDeepSearchResults(deep_search_response)

print(result.bathrooms) 