def get_gradio_space_url():
    """
    Returns the Gradio space URL for video generation.
    """
    return "https://bdc-divya-gradio-text-to-audio-generator.hf.space/--replicas/fackn/"

def get_iframe(video_url):
    """
    Returns an iframe HTML string for embedding the generated video.
    """
    return f"""
    <iframe src="{video_url}" width="640" height="480" frameborder="0" allowfullscreen></iframe>
    """
