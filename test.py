from gemini import Gemini

gemini = Gemini(model="gemini-2.5-flash")
prompt = "2*2-2 is 2 because 2*2 is 4 and 4-2 is 2. and current president of uzb is sh.mirzyoyev. and can you solve 3-12/6"
res = gemini.generate(prompt)
print(res)