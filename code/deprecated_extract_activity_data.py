# Function for retrieving the website and extracting the relevant information
def extract_activity_data():
    response = requests.get(runnersite)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    activities = []
    today = datetime.today().strftime('%d.%m.%Y')
    
    # Find all lines with running activities
    activity_rows = soup.find_all('tr', class_='r')
    
    data = {
        'date': [],
        'a_type': [],
        'r_type': [],
        'distance': [],
        'duration': [],
        'pace': []
    }
    
    current_date = None
    
    for row in activity_rows:
        cols = row.find_all('td')
        
        if cols:
            date_cell = cols[1].text.strip()
            if date_cell == '': # completely empty means that it is not the first activity of the day
                offset = 0
            else:
                offset = 1
                new_date = date_cell.split()[0] + '.' + str(datetime.today().year)
                # Remember the date so that it can be used in lines without a date
                if new_date and new_date != current_date:
                    current_date = new_date
                    
            if row.find('i', class_='icons8-Running'):
                rt_str = cols[3 + offset].text.strip() if len(cols) > 3 + offset else ''
                distance_str = cols[4 + offset].text.strip().split()[0].replace(',', '.') if len(cols) > 4 + offset else ''
                duration_str = cols[5 + offset].text.strip() if len(cols) > 5 + offset else ''
                pace_str = cols[6 + offset].text.strip() if len(cols) > 6 + offset else ''
                
                # Check that the current values are not empty
                if distance_str and duration_str and pace_str:
                    activities.append({'date': current_date, 'a_type': 'run', 'r_type': rt_str, 'distance': distance_str, 'duration': duration_str, 'pace': pace_str})
                else:
                    # Use the previous date if the current values are empty
                    if data['date']:
                        activities.append({'date': data['date'][-1], 'a_type': 'run', 'r_type': rt_str, 'distance': distance_str, 'duration': duration_str, 'pace': pace_str})
    
    df = pd.DataFrame(activities)
#    dc.dataframe_to_sqlite(df, 'activities.db')
    df = df[df['a_type'] == 'run'] # Filter by activity type "run"
    
    # Clean up dataframe so that data types fit and do not cause errors later
    df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
    df['pace'] = df['pace'].str.replace("/km", "")  # Remove "/km"
    df['duration'] = pd.to_timedelta(df['duration'])
    df['duration_minutes'] = df['duration'].dt.total_seconds() / 60

    # Set new name for the final videoclip and the chartpic
    min_date_str = df['date'].min().replace('.', '')  # Format date without dots
    max_date_str = df['date'].max().replace('.', '')  # Format date without dots

    # Name the video file
    global final_video_clip
    final_video_clip = f"movies/activity_movie_{min_date_str}_{max_date_str}.mp4"
    global final_chart_pic
    final_chart_pic = f"movies/chart_{min_date_str}_{max_date_str}.png"
    
    # Give me the dataframe!
    return df