import litellm
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/example", tags=["Example Project"])


@router.get("/example", summary="Get a programming joke from Claude 3.5 Sonnet")
async def get_programming_joke():
    """
    Calls Claude 3.5 Sonnet on AWS Bedrock via litellm to get a programming
    joke and returns the response as a plain text string.
    """
    try:
        # Call the model using the AWS Bedrock model ID
        response = litellm.completion(
            model="anthropic.claude-3-haiku-20240307-v1:0",
            messages=[{"role": "user", "content": "Tell me a funny joke about programming. Just give me the joke, no additional text."}],
            caching=False,
            max_tokens=50,
            temperature=0.7,
        )
        
        # Extract the string content from the model's response
        joke = response.choices[0].message.content
        print(f"Joke received: {joke}")
        return joke.strip()

    except Exception as e:
        print(f"An error occurred while calling the model: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve a joke from the language model.",
        )