# In-memory dictionary to store URL mappings
url_store = {}

def get_shortcode(shortcode):
    return url_store.get(shortcode)

def save_shortcode(shortcode, url_mapping):
    url_store[shortcode] = url_mapping

def shortcode_exists(shortcode):
    return shortcode in url_store
