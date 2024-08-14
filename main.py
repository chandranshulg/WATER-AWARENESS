import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip

# HTML Content
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Save Water - Educate to Conserve</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }}
        header {{
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        section {{
            margin: 20px;
            padding: 20px;
            background-color: white;
            border-radius: 5px;
        }}
        h2 {{
            color: #4CAF50;
        }}
        ul {{
            list-style-type: square;
        }}
        footer {{
            text-align: center;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            position: fixed;
            bottom: 0;
            width: 100%;
        }}
        #video-container {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }}
        #video-container iframe {{
            width: 300px;
            height: 200px;
            margin: 10px;
        }}
        #poster-container {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }}
        #poster-container a {{
            display: block;
            margin: 10px;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
        }}
        #poster-container a:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Save Water, Secure Our Future</h1>
        <p>Learn how you can make a difference by conserving water.</p>
    </header>

    <section id="tips">
        <h2>Water Conservation Tips</h2>
        <ul>
            <li>Fix leaking taps and pipes.</li>
            <li>Use a bucket instead of a hose to wash your car.</li>
            <li>Install water-saving showerheads and faucets.</li>
            <li>Turn off the tap while brushing your teeth.</li>
            <li>Collect rainwater for gardening.</li>
        </ul>
    </section>

    <section id="videos">
        <h2>Educational Videos</h2>
        <div id="video-container">
            <video width="320" height="240" controls>
                <source src="water_saving_tips.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
    </section>

    <section id="posters">
        <h2>Downloadable Posters</h2>
        <div id="poster-container">
            <a href="poster1.png" download>Download Poster 1</a>
            <a href="poster2.png" download>Download Poster 2</a>
            <a href="poster3.png" download>Download Poster 3</a>
            <a href="poster4.png" download>Download Poster 4</a>
            <a href="poster5.png" download>Download Poster 5</a>
        </div>
    </section>

    <footer>
        <p>&copy; 2024 Save Water Campaign</p>
    </footer>
</body>
</html>
"""

# Poster generation
def create_poster(text, output_file):
    # Create an image with a white background
    img = Image.new('RGB', (800, 600), color=(255, 255, 255))

    # Load a font
    font = ImageFont.truetype("arial.ttf", 50)

    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)

    # Calculate text size and position
    text_width, text_height = draw.textsize(text, font=font)
    position = ((img.width - text_width) // 2, (img.height - text_height) // 2)

    # Draw text on image
    draw.text(position, text, fill="black", font=font)

    # Save the image
    img.save(output_file)

# Video generation
def create_video_slide(image_file, text, duration=5):
    # Create an image clip
    image_clip = ImageClip(image_file).set_duration(duration)

    # Create a text clip
    text_clip = TextClip(text, fontsize=70, color='white', bg_color='black')
    text_clip = text_clip.set_position('bottom').set_duration(duration)

    # Composite the image and text
    video = CompositeVideoClip([image_clip, text_clip])
    return video

def main():
    # Define tips
    tips = [
        "Fix leaking taps and pipes.",
        "Use a bucket instead of a hose to wash your car.",
        "Install water-saving showerheads and faucets.",
        "Turn off the tap while brushing your teeth.",
        "Collect rainwater for gardening."
    ]

    # Create posters
    print("Generating posters...")
    for i, tip in enumerate(tips):
        create_poster(tip, f"poster{i+1}.png")
    print("Posters generated successfully.")

    # Create video
    print("Generating video...")
    clips = []
    for i, tip in enumerate(tips):
        image_file = f"poster{i+1}.png"
        video_slide = create_video_slide(image_file, tip)
        clips.append(video_slide)

    # Concatenate all video slides
    final_video = concatenate_videoclips(clips)
    final_video.write_videofile("water_saving_tips.mp4", fps=24)
    print("Video generated successfully.")

    # Save the HTML file
    with open("index.html", "w") as f:
        f.write(HTML_CONTENT)

    print("Website files generated successfully.")
    print("All tasks completed.")

if __name__ == "__main__":
    main()
