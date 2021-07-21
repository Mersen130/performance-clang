f = open("res", "r")
while True:
	withhold = input("\nhit enter")
	line = f.readline().strip().split()
	if not line:
		print("script done")
	else:
		env = open(".env", "w")
		env.write("MODE=text\nURL={}\nBENCH_NAME={}".format(line[0], line[1]))
		env.close()
		print("wrote", line)
