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

    # Step 3: Calculate the height of text area and image area
    text_area_height = 840
    image_area_height = 1080
    
    # Step 4: Create the video writer object
    fps = 30 # video frame rate
    out = cv2.VideoWriter(final_video_clip, cv2.VideoWriter_fourcc(*'mp4v'), fps, (1080, 1920))

    # Step 5: Iterate through each clip and write to video
    for clip in clips:
        # Convert clip to numpy array
        frame_clip = clip.get_frame(0)

        # Resize clip to fit text area
        frame_clip_resized = cv2.resize(frame_clip, (1080, text_area_height))

        # Create image clip
        image_clip = cv2.imread(chart_file_pic)
        image_clip_resized = cv2.resize(image_clip, (1080, image_area_height))

        # Combine text and image area
        frame = np.vstack([frame_clip_resized, image_clip_resized])

        # Write frame to video
        out.write(frame)
    
    # Step 6: Calculate sums and averages
    distance_sum = df['distance'].sum()
    duration_sum = df['duration'].sum()
    pace_mean = df['pace'].apply(lambda x: datetime.strptime(x, '%M:%S')).mean().strftime('%M:%S')

    # Step 7: Write summary clip to video
    summary_text = f"Total:\n{distance_sum}\n{duration_sum}\n{pace_mean}"
    summary_clip = TextClip(summary_text, fontsize=20, color='white', bg_color='black').set_duration(final_duration)
    summary_frame = summary_clip.get_frame(0)
    summary_frame_resized = cv2.resize(summary_frame, (1080, text_area_height))
    final_frame = np.vstack([summary_frame_resized, image_clip_resized])  # Use last image clip
    out.write(final_frame)

    # Release video writer object
    out.release()