import os
import sys
import subprocess
import argparse
import time
import shutil
from pathlib import Path

def mock_render(output_dir: str, frame_start: int, frame_end: int, output_format: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # fake frames
    for f in range(frame_start, frame_end + 1):
        fake_frame = Path(output_dir) / f"frame_{f:05d}.png"
        fake_frame.write_bytes(b"FAKE_FRAME")
        time.sleep(0.03)

    if output_format.lower() == "mp4":
        fake_video = Path(output_dir) / "final.mp4"
        fake_video.write_bytes(b"FAKE_MP4")
        return str(fake_video)

    return output_dir

def render(blend_file, frame_start, frame_end, resolution, output_format, output_dir, mock=False):
    print(f"Starting render for {blend_file} frames {frame_start}-{frame_end}")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Resolution mapping
    res_map = {
        '720p': ('1280', '720'),
        '1080p': ('1920', '1080'),
        '4k': ('3840', '2160')
    }
    width, height = res_map.get(resolution, ('1920', '1080'))
    
    output_path = os.path.join(output_dir, "frame_####")
    
    # Check if blender exists
    blender_cmd = shutil.which("blender")
    
    if blender_cmd and not mock:
        # Blender CLI command
        cmd = [
            blender_cmd,
            "-b", blend_file,
            "-o", output_path,
            "-F", "PNG",
            "-x", "1",
            "-s", str(frame_start),
            "-e", str(frame_end),
            "-a",
            "--", "--cycles-device", "CPU"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("Render complete")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            sys.exit(1)
            
        # Real FFmpeg conversion
        if output_format == 'mp4':
            print("Converting to MP4...")
            final_mp4 = os.path.join(output_dir, "output.mp4")
            
            ffmpeg_cmd = shutil.which("ffmpeg")
            if ffmpeg_cmd:
                try:
                    cmd = [
                        ffmpeg_cmd,
                        "-framerate", "24",
                        "-i", os.path.join(output_dir, "frame_%04d.png"),
                        "-c:v", "libx264",
                        "-pix_fmt", "yuv420p",
                        final_mp4
                    ]
                    subprocess.run(cmd, check=True)
                    print("Conversion complete")
                except subprocess.CalledProcessError as e:
                    print(f"Error converting to mp4: {e}")
            else:
                print("ffmpeg not found. Skipping conversion.")

    else:
        if mock:
            print("Mock mode enabled. Simulating render process...")
        else:
            print("Blender not found. Simulating render process...")
        
        mock_render(output_dir, frame_start, frame_end, output_format)
        print("Render complete (simulated)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend_file", required=True)
    parser.add_argument("--frame_start", type=int, required=True)
    parser.add_argument("--frame_end", type=int, required=True)
    parser.add_argument("--resolution", default="1080p")
    parser.add_argument("--output_format", default="mp4")
    parser.add_argument("--output_dir", default="/render/output")
    parser.add_argument("--mock", action="store_true", help="Mock render mode (no Blender needed)")
    args = parser.parse_args()
    
    if args.mock:
        print("MOCK MODE: simulating render...")
        result = mock_render(args.output_dir, args.frame_start, args.frame_end, args.output_format)
        print("Mock render completed:", result)
        sys.exit(0)
    
    render(args.blend_file, args.frame_start, args.frame_end, args.resolution, args.output_format, args.output_dir, args.mock)
