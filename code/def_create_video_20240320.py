# Function for creating the video
def create_video(df):

    # Step 1: Determine the number of records in the DataFrame
    num_records = len(df)

    # Step 2: Optionally filter DataFrame rows by date range
    if video_start_date and video_end_date:
        df = df[(df['date'] >= video_start_date) & (df['date'] <= video_end_date)]

    # Step 3: Create text clips for each row in DataFrame
    clips = []
    for index, row in df.iterrows():
        text = f"Date: {row['date']}\nDistance: {row['distance']}\nDuration: {row['duration']}\nPace: {row['pace']}"
        clip = TextClip(text, fontsize=20, color='white', bg_color='black').set_duration(3)
        clips.append(clip)

    # Step 4: Concatenate text clips vertically
    text_clip = CompositeVideoClip(clips, size=(1920, 540)).set_position(("center", "top"))

    # Step 5: Calculate sums and averages
    distance_sum = df['distance'].sum()
    duration_sum = df['duration'].sum()
    pace_mean = df['pace'].apply(lambda x: datetime.strptime(x, '%M:%S')).mean()

    # Create text clip for sums and averages
    summary_text = f"Total Distance: {distance_sum}\nTotal Duration: {duration_sum}\nAverage Pace: {pace_mean}"
    summary_clip = TextClip(summary_text, fontsize=20, color='white', bg_color='black').set_duration(7).set_position(("center", "bottom"))

    # Step 6: Optionally add start and end graphics
    clips_to_concatenate = []
    if video_start_graphic:
        start_clip = VideoClip(video_start_graphic).set_duration(start_clip_duration)  # Adjust duration as needed
        clips_to_concatenate.append(start_clip)
    clips_to_concatenate.extend([text_clip, summary_clip])
    if video_end_graphic:
        end_clip = VideoClip(video_end_graphic).set_duration(end_clip_duration)  # Adjust duration as needed

    # Step 7: Load chart pic and resize it
    square_graphic_clip = ImageClip(chart_file_pic).set_duration(10).resize(height=1080).set_position(("center", "bottom"))

    # Step 8: Concatenate all clips
    final_clip = concatenate_videoclips([text_clip, square_graphic_clip, summary_clip], method="compose")
    #clips_to_concatenate.append(end_clip)

    # Export final video
    final_clip.write_videofile(final_video_clip, fps=24, codec='libx264')