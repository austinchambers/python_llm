# Oculus-AR-Unity
Simple demonstration project for augmented reality with the OvrVision stereo camera and the Oculus Rift. 

# Python script to generate AI response for any of three providers: anthropic, openai, or mistral 

# To set up development environment and run
1. Install Python and the required SDKs: 
     * pip install anthropic openai 
     * pip install mistralai==0.4.2
     * python -m pip install python-dotenv
2. Set your API keys as environment variables or pass them with the --api-key flag
     * set ANTHROPIC_API_KEY=your_anthropic_api_key
     * set OPENAI_API_KEY=your_openai_api_key
     * set MISTRAL_API_KEY=your_mistral_api_key
3. Run the script (any of the following will work): 
     * python python_llm.py
     * python python_llm.py --provider anthropic
     * python python_llm.py --provider openai
     * python python_llm.py --provider mistral
     * python python_llm.py --provider openai --model gpt-4
     * python python_llm.py --provider mistral --model mistral-large-latest



# Getting Started
1. Plug in your OvrVision and your Oculus Rift
2. Install OpenCV
3. Print out "marker_aruco_64.pdf"
4. Open and run the project in Unity
5. Put on your headset and look at the marker. 
