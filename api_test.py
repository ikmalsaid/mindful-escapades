import google.generativeai as genai
import dotenv
import os

dotenv.load_dotenv()

genai.configure(api_key=os.environ["GEMINI_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("Write a poem about coffee versus tea.")

print(response.text)

# The kettle sings, the water boils,    
# A battle brews, a choice it spoils.   
# One dark and bold, the other bright,  
# Coffee and tea, a morning fight.      

# The coffee bean, a roasted heart,     
# A bitter truth, a fiery start.        
# It wakes the soul, a potent brew,     
# A jolt of life, a morning hue.        

# The tea leaf, delicate and fine,      
# A fragrant dance, a taste divine.     
# It calms the nerves, a gentle hand,   
# A soothing balm, across the land.     

# Coffee screams, a bold command,       
# "Awake! Be strong, you're in my hand!"
# While tea whispers, soft and low,
# "Relax, unwind, let feelings flow."

# The choice is yours, a personal quest,
# Which will you choose, to be your best?
# A bitter edge, a gentle grace,
# A morning ritual, in time and space.

# So raise a cup, a toast we share,
# To coffee's fire, and tea's sweet care.
# May both delight, in morning's light,
# And fill your day with warmth and might.