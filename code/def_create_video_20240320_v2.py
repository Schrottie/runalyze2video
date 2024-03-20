# Function for creating the video
def create_video(df):

    # Step 1: Optionally filter DataFrame rows by date range
    if video_start_date and video_end_date:
        df = df[(df['date'] >= video_start_date) & (df['date'] <= video_end_date)]

    # Step 2: Create text clips for each row in DataFrame
    clips = []
    for index, row in df.iterrows():
        text = f"{row['date']}\n{row['distance']}\n{row['duration']}\n{row['pace']}"
        clip = TextClip(text, fontsize=20, color='white', bg_color='black').set_duration(duration_per_row)
        clips.append(clip)

    # Step 3: Concatenate text clips vertically
    text_clip = concatenate_videoclips(clips, method="compose").resize(width=1080).set_position(("center", "top"))

    # Step 4: Calculate sums and averages
    distance_sum = df['distance'].sum()
    duration_sum = df['duration'].sum()
    pace_mean = df['pace'].apply(lambda x: datetime.strptime(x, '%M:%S')).mean().strftime('%M:%S')

    # Create text clip for sums and averages
    summary_text = f"Total:\n{distance_sum}\n{duration_sum}\n{pace_mean}"
    summary_clip = TextClip(summary_text, fontsize=20, color='white', bg_color='black').set_duration(final_duration).set_position(("center", "bottom"))

    # Step 5: Load chart pic and resize it
    square_graphic_clip = ImageClip(chart_file_pic).set_duration(10).resize(width=1080).set_position(("center", "bottom"))

    # Step 6: Concatenate all clips
    final_clip = concatenate_videoclips([text_clip.set_duration(15), square_graphic_clip.set_duration(10), summary_clip.set_duration(7)], method="compose")

    # Export final video
    final_clip.write_videofile(final_video_clip, fps=24, codec='libx264')