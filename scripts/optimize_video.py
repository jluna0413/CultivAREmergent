import os
from moviepy import VideoFileClip

input_path = r"a:\dev\CultivAREmergant\flutter_app\assets\videos\landing_video.mp4"
output_path = r"a:\dev\CultivAREmergant\flutter_app\assets\videos\landing_video_optimized.mp4"

def optimize():
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return

    print(f"Processing {input_path}...")
    try:
        # Load clip
        clip = VideoFileClip(input_path)
        print(f"Original resolution: {clip.w}x{clip.h}")
        print(f"Original duration: {clip.duration}s")

        # Resize if height > 540
        final_clip = clip
        if clip.h > 540:
            print("Resizing to 540p...")
            final_clip = clip.resized(height=540) # MoviePy v2
        
        # Write output
        # codec libx264, crf 32 for aggressive compression (mobile background)
        print("Writing optimized file...")
        final_clip.write_videofile(
            output_path,
            codec='libx264',
            audio=False,
            preset='faster',
            ffmpeg_params=['-crf', '32']
        )
        
        clip.close()
        final_clip.close()
        print(f"Done. Saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Fallback for method name if 'resized' fails
        if "'VideoFileClip' object has no attribute 'resized'" in str(e):
             print("Retrying with .resize() method...")
             try:
                 clip = VideoFileClip(input_path)
                 final_clip = clip.resize(height=720)
                 final_clip.write_videofile(output_path, codec='libx264', audio=False, preset='faster', ffmpeg_params=['-crf', '28'])
                 clip.close()
                 final_clip.close()
             except Exception as e2:
                 print(f"Retry failed: {e2}")

if __name__ == "__main__":
    optimize()
