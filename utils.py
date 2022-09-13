import unidecode

def normalize_csv_header(header):

    normalized_header = []
    for h in header:
        normalized_header.append(unidecode.unidecode(h.replace(' ', '_').replace(')','').replace('(', '').lower().strip()))

    return normalized_header