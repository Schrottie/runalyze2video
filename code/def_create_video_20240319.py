# Function for creating the video
def create_video(activities):

    # Create text for the final display
    sum_text = f"Total: Distance {activities['distance'].sum()} km, Duration {activities['duration'].sum()}, Pace {activities['pace'].apply(lambda x: datetime.strptime(x, '%M:%S')).mean()}"
    
    # Create the clip for the chart
    chart_clip = (ImageClip(resize_with_antialiasing(cv2.imread(chart_file_pic), (width, height // 2)))
               .set_duration(duration_per_row * len(activities))
               .set_position(('center', 'bottom')))

    # Create clips for data rows
    data_clips = []
    for i, (_, row) in enumerate(activities.iterrows()):
        text = f"Date: {row['date']} - Distance: {row['distance']} km - Duration: {row['duration']} - Pace: {row['pace']}"
        data_clips.append(text)

    # Create temporary text file
    with open(video_data_file, 'w') as file:
        file.write('\n'.join(data_clips))

    # Generate the final command for ffmpeg -- Change ffmpeg_path to 'ffmpeg' if ffmpeg is in PATH
    ffmpeg_command = [
        ffmpeg_path, '-y', '-loop', '1', '-i', chart_file_pic, '-vf',
        f"drawtext=fontsize=40:fontcolor=white:fontfile=Arial.ttf:textfile={video_data_file}:y=h-line_h-10:x=w/2-tw/2:reload=1",
        '-t', str(duration_per_row * len(activities)), '-pix_fmt', 'yuv420p', chart_file_vid
    ]

    # Execute ffmpeg command
    subprocess.run(ffmpeg_command)
    
    # Wait until the videofile is created
    #wait_for_file_creation(chart_file_vid)
    
    # Concatenate chart video with final display
    final_clip = concatenate_videoclips([VideoFileClip(chart_file_vid), TextClip(sum_text, fontsize=70, color='white', bg_color='black').set_duration(final_duration)])

    # Resize final clip
    final_clip = final_clip.resize(width=width)

    # Save the final video
    final_clip.write_videofile(final_video_clip, fps=24, codec='libx264')

    # Clean up temporary files
    os.remove(chart_file_pic)
    os.remove(video_data_file)
    os.remove(chart_file_vid)