import pandas as pd
import re

def GrabGoogleSheet(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)

    return new_url


# loc = "https://docs.google.com/spreadsheets/d/1mSEJtzy5L0nuIMRlY9rYdC5s899Ptu2gdMJcIalr5pg/edit#gid=1606352415"
# # Replace with your modified URL
# url = "https://docs.google.com/spreadsheets/d/1I_Bih_G4gx1wPw7Hv7ENS-OwPCKoPhm5IigsyaioPyE/edit?gid=0#gid=0"
# new_url = GrabGoogleSheet(url)
# df = pd.read_csv(new_url)
# df.loc[1] = ["c", "r"]

