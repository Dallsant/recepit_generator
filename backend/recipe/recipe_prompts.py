recipe_generation_prompt = """
                            Act as a recipe generator, given a list of ingridients, generate a list of recipes that " \
                           "includes their name, description, a list of ingridientes, and the directions on how to " \
                           "generate them in JSON format. If strict mode is enabled, only use ingredients from " \
                           "the list. And structure the output based on the parameters given. Make sure to generate the \ 
                           output on the language given in the output_language params  \n\nExample:\n\n
                            parameters = ${EXAMPLE_PARAMETERS} \
                           \n\nOUTPUT:\n\n{\"recipes\": [{\"name\":\"REESE'S " \
                           "STUFFED OREOS\",\"description\":\"Stuffes oreos with peanut butter " \
                           "filling\".\"ingredients\": [\"Double Stuffed Oreos\",\"Full Sized Reese's Peanut Butter " \
                           "Cups\",\"Melted Chocolate\",\"You can use the Vanilla Oreos and White Chocolate Too\"]," \
                           "\"directions\": [\"Twist apart the Oreos - separate the ones WITH icing to use for the " \
                           "sandwiches. The ones WITHOUT icing for toppings.\",\"Place the Reese's Cup between the " \
                           "Oreos, Give them a little squeeze so the filling sticks to the cup.\",\"Melt the " \
                           "Chocolate - then dip the sandwich in the Melted Chocolate. You can add a little " \
                           "shortening to thin it out. Use a fork to keep them pretty.\",\"Garnish with some MORE " \
                           "crushed Oreos\",\"Use the fork to remove the oreo from the chocolate, tap it on the edge " \
                           "of the bowl a few times (to let excess chocolate drip off) and transfer to a lined cookie " \
                           "sheet.\",\"Leave at room temperature until set.\",\"you don't have to scrape the icing " \
                           "off if you want the extra flavor.\"]},}\n\n
                           parameters = ${PARAMETERS}
                           
                           \nOUTPUT:\n\n 
                           """