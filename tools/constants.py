import os
import geonamescache

def filenamer(path):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ROOT_DIR, '../' + path)

msa_state_dic = {
    '12060': ['13'],
    '12420': ['48'],
    '12580': ['24'],
    '13820': ['01'],
    '15380': ['36'],
    '17460': ['39'],
    '18140': ['39'],
    '19100': ['48'],
    '19740': ['08'],
    '19820': ['26'],
    '25540': ['09'],
    '26420': ['48'],
    '26900': ['18'],
    '27260': ['12'],
    '29820': ['32'],
    '31080': ['06'],
    '33100': ['12'],
    '33340': ['55'],
    '34980': ['47'],
    '35380': ['22'],
    '36420': ['40'],
    '36740': ['12'],
    '38060': ['04'],
    '38300': ['42'],
    '39580': ['37'],
    '40060': ['51'],
    '40140': ['06'],
    '40900': ['06'],
    '41620': ['49'],
    '41700': ['48'],
    '41740': ['06'],
    '41860': ['06'],
    '41940': ['06'],
    '42660': ['53'],
    '45300': ['12'],
    '47900': ['11', '24', '54', '51'],
    '47260': ['37', '51'],
    '41180': ['17', '29'],
    '39300': ['25', '44'],
    '38900': ['41', '53'],
    '35620': ['34', '36', '42'],
    '14460': ['25', '33'],
    '16740': ['37', '45'],
    '16980': ['17', '18', '55'],
    '17140': ['18', '21', '39'],
    '28140': ['20', '29'],
    '31140': ['18', '21'],
    '32820': ['05', '28', '47'],
    '33460': ['27', '55'],
    '37980': ['24', '34', '10', '42']
}

us_abb_fips_codes_dic = {'US': '00'}
us_fips_codes_abb_dic = {'00': 'US'}
us_abb_names_dic = {'US': 'United States'}
us_names_abb_dic = {'US': 'United States'}

state_abb_fips_codes_dic = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}
state_fips_codes_abb_dic = dict(map(reversed, state_abb_fips_codes_dic.items()))

state_abb_state_names_dic = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming',
}
state_name_state_abb_dic = dict(map(reversed, state_abb_state_names_dic.items()))

msa_fips_codes_names_dic = {
    '12060': 'Atlanta-Sandy Springs-Roswell, GA',
    '12420': 'Austin-Round Rock, TX',
    '12580': 'Baltimore-Columbia-Towson, MD',
    '13820': 'Birmingham-Hoover, AL',
    '15380': 'Buffalo-Cheektowaga-Niagara Falls, NY',
    '17460': 'Cleveland-Elyria, OH',
    '18140': 'Columbus, OH',
    '19100': 'Dallas-Fort Worth-Arlington, TX',
    '19740': 'Denver-Aurora-Lakewood, CO',
    '19820': 'Detroit-Warren-Dearborn, MI',
    '25540': 'Hartford-West Hartford-East Hartford, CT',
    '26420': 'Houston-The Woodlands-Sugar Land, TX',
    '26900': 'Indianapolis-Carmel-Anderson, IN',
    '27260': 'Jacksonville, FL',
    '29820': 'Las Vegas-Henderson-Paradise, NV',
    '31080': 'Los Angeles-Long Beach-Anaheim, CA',
    '33100': 'Miami-Fort Lauderdale-West Palm Beach, FL',
    '33340': 'Milwaukee-Waukesha-West Allis, WI',
    '34980': 'Nashville-Davidson--Murfreesboro--Franklin, TN',
    '35380': 'New Orleans-Metairie, LA',
    '36420': 'Oklahoma City, OK',
    '36740': 'Orlando-Kissimmee-Sanford, FL',
    '38060': 'Phoenix-Mesa-Scottsdale, AZ',
    '38300': 'Pittsburgh, PA',
    '39580': 'Raleigh, NC',
    '40060': 'Richmond, VA',
    '40140': 'Riverside-San Bernardino-Ontario, CA',
    '40900': 'Sacramento--Roseville--Arden-Arcade, CA',
    '41620': 'Salt Lake City, UT',
    '41700': 'San Antonio-New Braunfels, TX',
    '41740': 'San Diego-Carlsbad, CA',
    '41860': 'San Francisco-Oakland-Hayward, CA',
    '41940': 'San Jose-Sunnyvale-Santa Clara, CA',
    '42660': 'Seattle-Tacoma-Bellevue, WA',
    '45300': 'Tampa-St. Petersburg-Clearwater, FL',
    '47900': 'Washington-Arlington-Alexandria, DC-VA-MD-WV',
    '47260': 'Virginia Beach-Norfolk-Newport News, VA-NC',
    '41180': 'St. Louis, MO-IL',
    '39300': 'Providence-Warwick, RI-MA',
    '38900': 'Portland-Vancouver-Hillsboro, OR-WA',
    '35620': 'New York-Newark-Jersey City, NY-NJ-PA',
    '14460': 'Boston-Cambridge-Newton, MA-NH',
    '16740': 'Charlotte-Concord-Gastonia, NC-SC',
    '16980': 'Chicago-Naperville-Elgin, IL-IN-WI',
    '17140': 'Cincinnati, OH-KY-IN',
    '28140': 'Kansas City, MO-KS',
    '31140': 'Louisville/Jefferson County, KY-IN',
    '32820': 'Memphis, TN-MS-AR',
    '33460': 'Minneapolis-St. Paul-Bloomington, MN-WI',
    '37980': 'Philadelphia-Camden-Wilmington, PA-NJ-DE-MD'
}

all_fips_name_dict = {
    '00': 'United States',
    **{k: state_abb_state_names_dic[v] for k, v in state_fips_codes_abb_dic.items() if v != 'PR'},
    **msa_fips_codes_names_dic,
    **{dict['fips']: dict['name'] for dict in geonamescache.GeonamesCache().get_us_counties()}
}

index_vars_dict = {
    'contribution': {'polarity': 'pos'},
    'compensation': {'polarity': 'pos'},
    'constancy': {'polarity': 'pos'}
}

age_category_dict = {
    0: 'Total',
    1: 'Ages 0 to 1',
    2: 'Ages 2 to 3',
    3: 'Ages 4 to 5',
    4: 'Ages 6 to 10',
    5: 'Ages 11+'
}

## constants to update
# qwi_start_year = 2004
# qwi_end_year = 2019
